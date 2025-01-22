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

"""API for providing dynamic inputs to NeuralGCM models."""

import abc
import functools

from flax import nnx
import jax
import jax.numpy as jnp

from neuralgcm.experimental import coordax as cx
from neuralgcm.experimental import typing


class DynamicInputValue(nnx.Intermediate):
  ...


class DynamicInputModule(nnx.Module, abc.ABC):
  """Base class for modules that interface with dynamically supplied data."""

  @abc.abstractmethod
  def update_dynamic_inputs(self, dynamic_inputs):
    """Ingests relevant data from `dynamic_inputs` onto the internal state."""
    raise NotImplementedError()

  @abc.abstractmethod
  def output_shapes(self) -> typing.Pytree:
    raise NotImplementedError()

  @abc.abstractmethod
  def __call__(self, sim_time: float) -> typing.Pytree:
    """Returns dynamic data at the specified sim_time."""
    raise NotImplementedError()


class DynamicInputSlice(DynamicInputModule):
  """Exposes inputs from the most recent available time slice."""

  def __init__(
      self,
      keys_to_coords: dict[str, cx.Coordinate],
      time_axis: int = 0,
  ):
    self.keys_to_coords = keys_to_coords
    self.time_axis = time_axis

  def update_dynamic_inputs(self, dynamic_inputs):
    # TODO(dkochkov): check that data aligns with expected data_specs.
    self.times = DynamicInputValue({
        k: dynamic_inputs[k].timestamp
        for k in self.keys_to_coords.keys()
    })
    self.data = DynamicInputValue(
        {k: dynamic_inputs[k].field.data for k in self.keys_to_coords.keys()}
    )

  def output_shapes(self) -> typing.Pytree:
    return {
        k: typing.ShapeFloatStruct(v.shape)
        for k, v in self.keys_to_coords.items()
    }

  def __call__(
      self,
      sim_time: float,
  ) -> typing.Pytree:
    """Returns covariates at the specified sim_time."""
    outputs = {}
    for k, time in self.times.value.items():  # pylint: disable=attribute-error
      time_indices = jnp.arange(time.size)
      approx_index = jnp.interp(sim_time, time, time_indices)
      index = jnp.round(approx_index).astype('int32')
      field_index_fn = functools.partial(
          jax.lax.dynamic_index_in_dim,
          index=index,
          axis=self.time_axis,
          keepdims=False,
      )
      # TODO(shoyer): use coordax.cmap instead of unwrapping the field.
      sliced_data = field_index_fn(self.data.value[k])
      outputs[k] = cx.wrap(sliced_data, self.keys_to_coords[k])
    return outputs
