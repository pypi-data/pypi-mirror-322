# Copyright (c) 2024 PaddlePaddle Authors. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
import tensorrt as trt

from paddle.tensorrt.converter_utils import (
    add_1D_constant_layer,
    add_cast_reduce_layer,
    add_elementwise_layer,
    add_reduce_layer,
    broadcast,
    cast_tensor,
    fill_constant_layer,
    get_axes_for_reduce_op,
    trt_cast,
    trt_expand,
    trt_max,
)
from paddle.tensorrt.register import converter_registry


@converter_registry.register("pd_op.add", trt_version="trt_version_ge=8.0")
@converter_registry.register("pd_op.add_", trt_version="trt_version_ge=8.0")
def add_converter(network, paddle_op, inputs):
    return add_elementwise_layer(
        network, paddle_op, inputs, trt.ElementWiseOperation.SUM
    )


@converter_registry.register("pd_op.scale", trt_version="trt_version_ge=8.0")
def scale_converter(network, paddle_op, inputs):
    x = inputs[0]
    bias = paddle_op.attrs().get("bias", 0.0)
    bias_after_scale = paddle_op.attrs().get("bias_after_scale", True)

    is_int = x.dtype == trt.int32
    if is_int:
        bias_tensor = add_1D_constant_layer(
            network, int(bias + 0.5) if bias > 0 else int(bias - 0.5)
        )
    else:
        bias_tensor = add_1D_constant_layer(network, bias, dtype=np.float32)
    is_bias_0 = bias == 0
    bias_shapes = [1] * len(x.shape)
    bias_shapes_tensor = add_1D_constant_layer(network, bias_shapes)
    reshape_layer_bias = network.add_shuffle(bias_tensor)
    reshape_layer_bias.set_input(1, bias_shapes_tensor)

    scale_op = paddle_op.operands()[1].source().get_defining_op()
    if scale_op.name() == "pd_op.full":
        scale = scale_op.attrs()["value"]
        has_scale_tensor = False
        if is_int:
            scale_tensor = add_1D_constant_layer(
                network, int(scale + 0.5 if scale > 0 else scale - 0.5)
            )
        else:
            scale_tensor = add_1D_constant_layer(
                network, scale, dtype=np.float32
            )
        is_scale_1 = scale == 1
    else:
        has_scale_tensor = True
        scale_tensor = inputs[1]
        is_scale_1 = False
    scale_shapes = [1] * len(x.shape)
    scale_shapes_tensor = add_1D_constant_layer(network, scale_shapes)
    reshape_layer_scale = network.add_shuffle(scale_tensor)
    reshape_layer_scale.set_input(1, scale_shapes_tensor)

    if has_scale_tensor and is_scale_1 and is_bias_0:
        layer = network.add_identity(x)
    else:
        if bias_after_scale:
            if not is_scale_1:
                layer = network.add_elementwise(
                    x,
                    reshape_layer_scale.get_output(0),
                    trt.ElementWiseOperation.PROD,
                )
                x = layer.get_output(0)

            if not is_bias_0:
                layer = network.add_elementwise(
                    x,
                    reshape_layer_bias.get_output(0),
                    trt.ElementWiseOperation.SUM,
                )

        else:
            if not is_bias_0:
                layer = network.add_elementwise(
                    x,
                    reshape_layer_bias.get_output(0),
                    trt.ElementWiseOperation.SUM,
                )
                x = layer.get_output(0)
            if not is_scale_1:
                layer = network.add_elementwise(
                    x,
                    reshape_layer_scale.get_output(0),
                    trt.ElementWiseOperation.PROD,
                )

    return layer.get_output(0)


@converter_registry.register("pd_op.max", trt_version="trt_version_ge=8.0")
def max_converter(network, paddle_op, inputs):
    input_tensor = inputs[0]
    axis = paddle_op.operands()[1].source().get_defining_op().attrs()["value"]
    input_shape = input_tensor.shape
    keepdim = paddle_op.attrs()["keepdim"]
    if network.has_implicit_batch_dimension:
        assert (
            axis != 0
        ), "can't reduce on axis == 0 when network has implicit batch dimension"
    output_shape = []
    if len(axis) == 0:
        axis = list(range(len(input_shape)))
    for i in range(len(axis)):
        if axis[i] < 0:
            axis[i] = len(input_shape) + axis[i]
    layer = network.add_reduce(
        input_tensor,
        trt.ReduceOperation.MAX,
        axes=get_axes_for_reduce_op(axis),
        keep_dims=keepdim,
    )
    return layer.get_output(0)


@converter_registry.register("pd_op.divide", trt_version="trt_version_ge=8.0")
def divide_converter(network, paddle_op, inputs):
    return add_elementwise_layer(
        network, paddle_op, inputs, trt.ElementWiseOperation.DIV
    )


@converter_registry.register("pd_op.subtract", trt_version="trt_version_ge=8.0")
def substract_converter(network, paddle_op, inputs):
    return add_elementwise_layer(
        network, paddle_op, inputs, trt.ElementWiseOperation.SUB
    )


@converter_registry.register("pd_op.multiply", trt_version="trt_version_ge=8.0")
def multiply_converter(network, paddle_op, inputs):
    return add_elementwise_layer(
        network, paddle_op, inputs, trt.ElementWiseOperation.PROD
    )


@converter_registry.register("pd_op.clip", trt_version="8.x")
def clip_converter(network, paddle_op, inputs):
    def _get_constant_or_expand_tensor(
        op, constant_inputs, input_shape_tensor, rank
    ):
        if op.name() == "pd_op.full":
            value = op.attrs()["value"]
            return fill_constant_layer(
                network, input_shape_tensor, rank, value, input_tensor.dtype
            )
        else:
            expanded_tensor = trt_expand(
                network, constant_inputs, 1, input_shape_tensor, rank
            )
            if expanded_tensor.dtype != input_tensor.dtype:
                expanded_tensor = cast_tensor(
                    network, expanded_tensor, input_tensor.dtype
                )
            return expanded_tensor

    input_tensor = inputs[0]
    input_shape = input_tensor.shape
    rank = len(input_shape)
    input_shape_tensor = network.add_shape(input_tensor).get_output(0)

    # handle min operation
    min_op = paddle_op.operands()[1].source().get_defining_op()
    alpha_t = _get_constant_or_expand_tensor(
        min_op, inputs[1], input_shape_tensor, rank
    )

    # handle max operation
    max_op = paddle_op.operands()[2].source().get_defining_op()
    beta_t = _get_constant_or_expand_tensor(
        max_op, inputs[2], input_shape_tensor, rank
    )

    # run the clip operation
    lower_clip = trt_max(network, input_tensor, alpha_t)
    layer = network.add_elementwise(
        lower_clip, beta_t, trt.ElementWiseOperation.MIN
    )
    return layer.get_output(0)


@converter_registry.register("pd_op.remainder", trt_version="8.x")
@converter_registry.register("pd_op.remainder_", trt_version="8.x")
def remainder_converter(network, paddle_op, inputs):
    from paddle.tensorrt.util import support_fp32_mix_precision

    weight_shape = paddle_op.operands()[1].source().shape
    input_shape = inputs[0].shape

    weight_tensor = inputs[1]
    input_tensor = inputs[0]
    if type(inputs[1]) == trt.Weights:
        weight_tensor = network.add_constant(
            weight_shape, inputs[1]
        ).get_output(0)
    if type(inputs[0]) == trt.Weights:
        input_tensor = network.add_constant(input_shape, inputs[0]).get_output(
            0
        )

    lhs_val, rhs_val = broadcast(
        network,
        input_tensor,
        weight_tensor,
        input_tensor.name,
        weight_tensor.name,
    )
    is_floor_div = input_tensor.dtype != trt.DataType.INT32
    if is_floor_div:
        quotient_layer = network.add_elementwise(
            lhs_val, rhs_val, trt.ElementWiseOperation.FLOOR_DIV
        )
    else:
        quotient_layer = network.add_elementwise(
            lhs_val, rhs_val, trt.ElementWiseOperation.DIV
        )
    quotient = quotient_layer.get_output(0)
    support_fp32_mix_precision(paddle_op.name(), quotient_layer)

    # Multiply rhs by the quotient
    product_layer = network.add_elementwise(
        rhs_val, quotient, trt.ElementWiseOperation.PROD
    )
    product = product_layer.get_output(0)
    support_fp32_mix_precision(paddle_op.name(), product_layer)
    remainder_layer = network.add_elementwise(
        lhs_val, product, trt.ElementWiseOperation.SUB
    )
    remainder = remainder_layer.get_output(0)
    support_fp32_mix_precision(paddle_op.name(), remainder_layer)

    return remainder


@converter_registry.register("pd_op.min", trt_version="8.x")
def min_converter(network, paddle_op, inputs):
    return add_reduce_layer(network, paddle_op, inputs, trt.ReduceOperation.MIN)


@converter_registry.register("pd_op.sum", trt_version="8.x")
def sum_converter(network, paddle_op, inputs):
    return add_reduce_layer(network, paddle_op, inputs, trt.ReduceOperation.SUM)


@converter_registry.register("pd_op.any", trt_version="8.x")
def any_converter(network, paddle_op, inputs):
    return add_cast_reduce_layer(
        network, paddle_op, inputs, trt.ReduceOperation.MAX
    )


@converter_registry.register("pd_op.all", trt_version="8.x")
def all_converter(network, paddle_op, inputs):
    return add_cast_reduce_layer(
        network, paddle_op, inputs, trt.ReduceOperation.MIN
    )


@converter_registry.register("pd_op.floor_divide", trt_version="8.x")
def floor_divide_converter(network, paddle_op, inputs):
    return add_elementwise_layer(
        network, paddle_op, inputs, trt.ElementWiseOperation.FLOOR_DIV
    )


@converter_registry.register("pd_op.log", trt_version="8.x")
def sqrt_converter(network, paddle_op, inputs):
    input_tensor = trt_cast(network, inputs[0], trt.float32)
    layer = network.add_unary(input_tensor, trt.UnaryOperation.LOG)
    return layer.get_output(0)


@converter_registry.register("pd_op.maximum", trt_version="8.x")
def maximum_converter(network, paddle_op, inputs):
    max_layer = add_elementwise_layer(
        network, paddle_op, inputs, trt.ElementWiseOperation.MAX
    )
    return max_layer
