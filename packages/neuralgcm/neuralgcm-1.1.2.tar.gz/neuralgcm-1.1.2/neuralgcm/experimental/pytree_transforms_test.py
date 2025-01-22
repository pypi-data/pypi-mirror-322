# Copyright 2024 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests that pytree_transforms work as expected and  pytrees with expected shapes."""

import functools
from typing import Any, Sequence

from absl.testing import absltest
from absl.testing import parameterized
import chex
from dinosaur import primitive_equations
from flax import nnx
import jax
import jax.numpy as jnp
from neuralgcm.experimental import coordax as cx
from neuralgcm.experimental import coordinates
from neuralgcm.experimental import data_specs
from neuralgcm.experimental import dynamic_io
from neuralgcm.experimental import orographies
from neuralgcm.experimental import pytree_mappings
from neuralgcm.experimental import pytree_transforms
from neuralgcm.experimental import pytree_utils
from neuralgcm.experimental import random_processes
from neuralgcm.experimental import standard_layers
from neuralgcm.experimental import towers
from neuralgcm.experimental import typing
from neuralgcm.experimental import units
import numpy as np
import xarray


class StandardPytreeTransformsTest(parameterized.TestCase):
  """Tests for standard_layers.MaskTransform and Composed.ConvLonLat."""

  @parameterized.parameters(
      dict(
          fields_to_mask=['u', 'v', 'T'],
          mask_shape=(5, 5),
          fill_value_true=0.0,
          fill_value_false=1.0,
          fill_threshold=jnp.nan,
      ),
      dict(
          fields_to_mask=['T'],
          mask_shape=(5, 5),
          fill_value_true=0.0,
          fill_value_false=1.0,
          fill_threshold=0.1,
      ),
      dict(
          fields_to_mask=['T'],
          mask_shape=(5, 5),
          fill_value_true=0.0,
          fill_value_false=1.0,
          fill_threshold=0.3,
      ),
  )
  def test_mask_transform(
      self,
      fields_to_mask: Sequence[str],
      mask_shape: tuple[int, int],
      fill_value_true: float,
      fill_value_false: float,
      fill_threshold: float,
  ):
    if fill_threshold is np.nan:
      nan_threshold = True
      threshold = 0.7
    else:
      nan_threshold = False
      threshold = fill_threshold
    data = {
        'u': ((np.arange(np.prod(mask_shape)) % 10) / 10).reshape(mask_shape),
        'v': ((np.arange(np.prod(mask_shape)) % 10) / 10).reshape(mask_shape),
        'T': ((np.arange(np.prod(mask_shape)) % 10) / 10).reshape(mask_shape),
    }
    expected = {
        k: (
            np.where(v > threshold, fill_value_true, fill_value_false)
            if k in fields_to_mask
            else v
        )
        for k, v in data.items()
    }
    if nan_threshold:
      inputs = {k: np.where(v > threshold, np.nan, v) for k, v in data.items()}
    else:
      inputs = data
    if len(mask_shape) == 2:
      xarray_test = xarray.Dataset(
          data_vars=dict(
              u=(['longitude', 'latitude'], inputs['u']),
              v=(['longitude', 'latitude'], inputs['v']),
              T=(['longitude', 'latitude'], inputs['T']),
          ),
          coords=dict(
              longitude=('longitude', np.arange(mask_shape[-2])),
              latitude=('latitude', np.arange(mask_shape[-1])),
          ),
      )
    elif len(mask_shape) == 3:
      xarray_test = xarray.Dataset(
          data_vars=dict(
              u=(['longitude', 'latitude', 'level'], inputs['u']),
              v=(['longitude', 'latitude', 'level'], inputs['v']),
              T=(['longitude', 'latitude', 'level'], inputs['T']),
          ),
          coords=dict(
              longitude=('longitude', np.arange(mask_shape[-3])),
              latitude=('latitude', np.arange(mask_shape[-2])),
              level=('level', np.arange(mask_shape[-1])),
          ),
      )
    else:
      raise ValueError(f'Expected mask_shape of length 2 or 3. {mask_shape=}')
    mask_transform = pytree_transforms.MaskTransform(
        fields_to_mask=fields_to_mask,
        mask_shape=mask_shape,
        fill_value_true=fill_value_true,
        fill_value_false=fill_value_false,
        fill_threshold=fill_threshold,
    )

    with self.subTest('gen_mask_from_xarray'):
      mask_transform.update_from_xarray(xarray_test, fields_to_mask[0])
      np.testing.assert_allclose(
          mask_transform.mask.value, expected[fields_to_mask[0]]
      )

    test_data = {
        'u': np.ones(mask_shape),
        'v': np.ones(mask_shape),
        'T': np.ones(mask_shape),
    }
    with self.subTest('check_mask_applies_to_correct_variables'):
      outputs = mask_transform(test_data)
      for i in set(['u', 'v', 'T']) - set(fields_to_mask):
        np.testing.assert_allclose(outputs[i], np.ones(mask_shape))
      for i in fields_to_mask:
        np.testing.assert_allclose(outputs[i], expected[i])

  @parameterized.parameters(
      dict(
          input_dict={'a': 3, 'b': 4, 'c': 5},
          keys_to_nest=('b',),
          nested_key_name='nested_b',
          expected={'a': 3, 'nested_b': {'b': 4}, 'c': 5},
      ),
      dict(
          input_dict={'a': 3, 'b': 4, 'c': 5, '6': 6},
          keys_to_nest=('b', 'c', '6'),
          nested_key_name='tracers',
          expected={'a': 3, 'tracers': {'b': 4, 'c': 5, '6': 6}},
      ),
  )
  def test_nest_dict_transform(
      self,
      input_dict: Sequence[str],
      keys_to_nest: tuple[str, ...],
      nested_key_name: str,
      expected: dict[str, Any],
  ):
    nest_dict_transform = pytree_transforms.NestDict(
        keys_to_nest=keys_to_nest, nested_key_name=nested_key_name
    )
    actual = nest_dict_transform(input_dict)
    chex.assert_trees_all_equal(actual, expected)

  @parameterized.parameters(
      dict(n_clip=1),
      dict(n_clip=2),
      dict(n_clip=5),
  )
  def test_clip_wavenumbers(self, n_clip: int = 1):
    """Tests that ClipWavenumbers works as expected."""
    grid = coordinates.SphericalHarmonicGrid.T21()
    inputs = {
        'u': np.ones(grid.shape),
        'v': np.ones(grid.shape),
    }
    ls = grid.fields['total_wavenumber'].data
    clip_mask = (np.arange(ls.size) <= (ls.max() - n_clip)).astype(int)
    expected = jax.tree.map(lambda x: x * clip_mask, inputs)
    clip_transform = pytree_transforms.ClipWavenumbers(
        grid=grid, wavenumbers_to_clip=n_clip
    )
    actual = clip_transform(inputs)
    chex.assert_trees_all_equal(actual, expected)

  def test_batch_shift_and_normalize(self):
    """Tests that BatchShiftAndNormalize works as expected."""
    feature_size = 2
    batch_size = 200
    shape = (batch_size, feature_size)

    keys = ('a', 'b', 'c', 'd')
    input_means = (2.0, 0.0, -12.5, 100.0)
    input_stds = (0.2, 1.5, 3.14, 100.0)

    def get_inputs(rng):
      rngs = jax.random.split(rng, len(keys))
      return {
          k: jax.random.normal(rng, shape=shape) * std + mean
          for k, rng, mean, std in zip(keys, rngs, input_means, input_stds)
      }

    xs = get_inputs(jax.random.PRNGKey(1))

    def _check_mean_and_std(xs, expected_means, expected_stds):
      mean_over_batch = functools.partial(np.mean, axis=0)
      std_over_batch = functools.partial(np.std, axis=0)
      xs_mean = jax.tree.map(mean_over_batch, xs)
      xs_std = jax.tree.map(std_over_batch, xs)
      for i, k in enumerate(keys):
        mean_atol = 6 * (expected_stds[i] / np.sqrt(batch_size))
        std_atol = 6 * (np.sqrt(2 / (batch_size - 1)) * expected_stds[i]**2)
        expected_mean = np.array([expected_means[i]] * feature_size)
        expected_std = np.array([expected_stds[i]] * feature_size)
        np.testing.assert_allclose(xs_mean[k], expected_mean, atol=mean_atol)
        np.testing.assert_allclose(xs_std[k], expected_std, atol=std_atol)

    with self.subTest('input_mean_and_std'):
      _check_mean_and_std(xs, input_means, input_stds)

    batch_shift_and_normalize = pytree_transforms.BatchShiftAndNormalize(
        {k: feature_size for k in keys},
        feature_axis=-1,
        momentum=0.1,
        use_running_average=True,
    )
    with self.subTest('identity_at_init'):
      ys = batch_shift_and_normalize(xs)
      _check_mean_and_std(ys, input_means, input_stds)

    zero_means = tuple(0.0 for _ in input_means)
    unit_stds = tuple(1.0 for _ in input_stds)
    with self.subTest('zero_mean_unit_variance_when_dynamic'):
      batch_shift_and_normalize.use_running_average = False
      ys = batch_shift_and_normalize(xs)
      _check_mean_and_std(ys, zero_means, unit_stds)

    with self.subTest('converges_to_zero_mean_unit_variance'):
      for _ in range(20):  # EMA converges with remaining init bias ~0.1**20.
        _ = batch_shift_and_normalize(xs)
      batch_shift_and_normalize.use_running_average = True
      ys = batch_shift_and_normalize(xs)
      _check_mean_and_std(ys, zero_means, unit_stds)


class InputsFeaturesTest(parameterized.TestCase):
  """Tests input features modules."""

  def _test_feature_module(
      self,
      feature_module: pytree_transforms.Transform,
      inputs: typing.Pytree,
  ):
    with self.subTest('call method'):
      features = feature_module(inputs)

    with self.subTest('output_shape_matches_actual'):
      input_shapes = pytree_utils.shape_structure(inputs)
      actual = feature_module.output_shapes(input_shapes)
      expected = pytree_utils.shape_structure(features)
      chex.assert_trees_all_equal(actual, expected)

  @parameterized.named_parameters(
      dict(
          testcase_name='dinosaur_coords',
          coords=coordinates.DinosaurCoordinates(
              horizontal=coordinates.LonLatGrid.T21(),
              vertical=coordinates.SigmaLevels.equidistant(4),
          ),
      ),
  )
  def test_radiation_features(self, coords):
    radiation_features = pytree_transforms.RadiationFeatures(
        coords=coords,
        sim_units=units.DEFAULT_UNITS,
    )
    self._test_feature_module(
        radiation_features,
        {'sim_time': np.array(314.159)},
    )

  def test_latitude_features(self):
    grid = coordinates.LonLatGrid.T21()
    latitude_features = pytree_transforms.LatitudeFeatures(grid=grid)
    self._test_feature_module(latitude_features, None)

  def test_orography_features(self):
    grid = coordinates.SphericalHarmonicGrid.T21()
    orography = orographies.ModalOrography(grid=grid, rngs=None)
    orography_features = pytree_transforms.OrographyFeatures(
        orography_module=orography,
    )
    self._test_feature_module(orography_features, None)

  def test_orography_with_grads_features(self):
    grid = coordinates.SphericalHarmonicGrid.T21()
    orography = orographies.ModalOrography(grid=grid, rngs=None)
    orography_features = pytree_transforms.OrographyWithGradsFeatures(
        orography_module=orography,
        compute_gradients_transform=pytree_transforms.ToModalWithFilteredGradients(
            grid, filter_attenuations=[2.0]
        ),
    )
    self._test_feature_module(orography_features, None)

  def test_dynamic_input_features(self):
    grid = coordinates.LonLatGrid.T21()
    dynamic_input = dynamic_io.DynamicInputSlice(
        keys_to_coords={'a': grid, 'b': grid, 'c': grid}
    )
    expand_dims = lambda x: np.expand_dims(x, axis=(1, 2))
    data = {
        'a': expand_dims(np.arange(2)) * np.ones(grid.shape),
        'b': expand_dims(np.arange(2)) * np.zeros(grid.shape),
        'c': expand_dims(np.arange(2)) * np.ones(grid.shape),
    }
    timedelta = coordinates.TimeDelta.as_index(2)
    grid_trajectory = cx.compose_coordinates(timedelta, grid)
    sim_time = np.arange(timedelta.shape[0])
    in_data = {
        k: data_specs.TimedField(cx.wrap(v, grid_trajectory), sim_time)
        for k, v in data.items()
    }
    dynamic_input.update_dynamic_inputs(in_data)
    with self.subTest('two_keys'):
      dynamic_input_features = pytree_transforms.DynamicInputFeatures(
          ('a', 'b'), dynamic_input
      )
      self._test_feature_module(dynamic_input_features, {'sim_time': 0.1})

  def test_spatial_surface_features(self):
    feature_sizes = {
        'learned_surface_features': 8,
    }
    grid = coordinates.LonLatGrid.T21()
    static_surface_features = pytree_transforms.SpatialSurfaceFeatures(
        feature_sizes, grid=grid, rngs=nnx.Rngs(1)
    )
    self._test_feature_module(static_surface_features, None)

  def test_velocity_and_prognostics_with_modal_gradients(self):
    coords = coordinates.DinosaurCoordinates(
        horizontal=coordinates.LonLatGrid.T21(),
        vertical=coordinates.SigmaLevels.equidistant(3),
    )
    with_gradients_transform = pytree_transforms.ToModalWithFilteredGradients(
        coords.horizontal, filter_attenuations=[2.0]
    )
    features_grads = pytree_transforms.VelocityAndPrognosticsWithModalGradients(
        coords,
        volume_field_names=(
            'u',
            'v',
        ),
        surface_field_names=('lsp',),
        compute_gradients_transform=with_gradients_transform,
    )
    inputs = {
        'u': np.ones(coords.dinosaur_coords.modal_shape),
        'v': np.ones(coords.dinosaur_coords.modal_shape),
        'lsp': np.ones(coords.dinosaur_coords.modal_shape[1:])[np.newaxis, ...],
        'tracers': {},
        'sim_time': 0.0,
    }
    self._test_feature_module(features_grads, inputs)

  def test_surface_embedding_features(self):
    n_levels = 12
    coords = coordinates.DinosaurCoordinates(
        horizontal=coordinates.LonLatGrid.T21(),
        vertical=coordinates.LayerLevels(n_levels),
    )
    mlp_factory = functools.partial(
        standard_layers.MlpUniform, hidden_size=6, n_hidden_layers=2
    )
    tower_factory = functools.partial(
        towers.ColumnTower, column_net_factory=mlp_factory
    )
    mapping_factory = functools.partial(
        pytree_mappings.ChannelMapping,
        tower_factory=tower_factory,
    )
    feature_module = pytree_transforms.LatitudeFeatures(
        grid=coords.horizontal,
    )
    embedding_factory = functools.partial(
        pytree_mappings.Embedding,
        feature_module=feature_module,
        mapping_factory=mapping_factory,
        rngs=nnx.Rngs(0),
    )
    surface_embedding_features = pytree_transforms.SurfaceEmbeddingFeatures(
        coords=coords,
        embedding_sizes={'abc': 3, 'foo': 5},
        embedding_factory=embedding_factory,
    )
    self._test_feature_module(surface_embedding_features, None)

  def test_volume_embedding_features(self):
    n_levels = 12
    coords = coordinates.DinosaurCoordinates(
        horizontal=coordinates.LonLatGrid.T21(),
        vertical=coordinates.LayerLevels(n_levels),
    )
    mlp_factory = functools.partial(
        standard_layers.MlpUniform, hidden_size=6, n_hidden_layers=2
    )
    tower_factory = functools.partial(
        towers.ColumnTower, column_net_factory=mlp_factory
    )
    mapping_factory = functools.partial(
        pytree_mappings.ChannelMapping,
        tower_factory=tower_factory,
    )
    feature_module = pytree_transforms.LatitudeFeatures(
        grid=coords.horizontal,
    )
    embedding_factory = functools.partial(
        pytree_mappings.Embedding,
        feature_module=feature_module,
        mapping_factory=mapping_factory,
        rngs=nnx.Rngs(0),
    )
    surface_embedding_features = pytree_transforms.VolumeEmbeddingFeatures(
        coords=coords,
        embedding_names=('abc', 'fuz', 'bar'),
        embedding_factory=embedding_factory,
    )
    self._test_feature_module(surface_embedding_features, None)

  @parameterized.named_parameters(
      dict(
          testcase_name='T21_grid',
          grid=coordinates.LonLatGrid.T21(),
      ),
  )
  def test_randomness_features(self, grid):
    with self.subTest('gaussian_random_field'):
      random_process = random_processes.GaussianRandomField(
          grid=grid,  # instantiating here because uses jax at __init__.
          dt=1.0,
          sim_units=units.DEFAULT_UNITS,
          correlation_time=1.0,
          correlation_length=1.0,
          variance=1.0,
          rngs=nnx.Rngs(0),
      )
      random_process.unconditional_sample(jax.random.PRNGKey(0))
      randomness_features = pytree_transforms.RandomnessFeatures(
          random_process=random_process,
          grid=grid,
      )
      self._test_feature_module(randomness_features, None)

    with self.subTest('batched_gaussian_random_fields'):
      random_process = random_processes.BatchGaussianRandomField(
          grid=grid,  # instantiating here because uses jax at __init__.
          dt=1.0,
          sim_units=units.DEFAULT_UNITS,
          correlation_times=[1.0, 2.0],
          correlation_lengths=[0.6, 0.9],
          variances=[1.0, 1.0],
          rngs=nnx.Rngs(0),
      )
      random_process.unconditional_sample(jax.random.PRNGKey(0))
      randomness_features = pytree_transforms.RandomnessFeatures(
          random_process=random_process,
          grid=grid,
      )
      self._test_feature_module(randomness_features, None)

  def test_prognostic_features(self):
    coords = coordinates.DinosaurCoordinates(
        horizontal=coordinates.LonLatGrid.T21(),
        vertical=coordinates.LayerLevels(n_layers=3),
    )
    prognostic_features = pytree_transforms.PrognosticFeatures(
        coords=coords, surface_field_names=('a', 'b'), volume_field_names=('c',)
    )
    inputs = {
        'a': np.ones((1,) + coords.horizontal.shape),
        'b': np.ones((1,) + coords.horizontal.shape),
        'c': np.ones(coords.shape),
        'sim_time': 0.0,
    }
    self._test_feature_module(prognostic_features, inputs)

  def test_pressure_features(self):
    coords = coordinates.DinosaurCoordinates(
        horizontal=coordinates.SphericalHarmonicGrid.T21(),
        vertical=coordinates.SigmaLevels.equidistant(8),
    )
    pressure_features = pytree_transforms.PressureFeatures(coords=coords)
    inputs = {
        'log_surface_pressure': np.ones((1,) + coords.horizontal.shape),
    }
    self._test_feature_module(pressure_features, inputs)


class PrecipitationminusEvaporationTest(parameterized.TestCase):
  """Tests PrecipitationminusEvaporation calculations."""

  def test_shape_and_value(self):
    """Tests that the output dimensions and values are correct."""
    sim_units = units.DEFAULT_UNITS
    coords = coordinates.DinosaurCoordinates(
        horizontal=coordinates.LonLatGrid.T21(),
        vertical=coordinates.SigmaLevels.equidistant(layers=8),
    )
    state = primitive_equations.State(
        divergence=np.ones(coords.shape),
        vorticity=np.ones(coords.shape),
        log_surface_pressure=np.zeros(coords.horizontal.shape),
        temperature_variation=np.ones(coords.shape),
        tracers={
            'specific_humidity': np.ones(coords.shape),
            'specific_cloud_ice_water_content': np.ones(coords.shape),
            'specific_cloud_liquid_water_content': np.ones(
                coords.shape
            ),
        },
    )
    expected_outputs = (
        np.ones(coords.horizontal.shape)
        * 3
        / sim_units.gravity_acceleration
    )

    pme = pytree_transforms.PrecipitationMinusEvaporation(
        grid=coords.horizontal,
        level=coords.vertical,
        sim_units=sim_units,
    )
    input_state_modal = coords.horizontal.ylm_grid.to_modal(state)
    inputs_tendency_modal = coords.horizontal.ylm_grid.to_modal(state)
    outputs = pme(tendencies=inputs_tendency_modal, state=input_state_modal)

    with self.subTest('shape'):
      self.assertEqual(outputs.shape, expected_outputs.shape)

    with self.subTest('value'):
      np.testing.assert_allclose(outputs, expected_outputs, rtol=1e-5)

if __name__ == '__main__':
  absltest.main()
