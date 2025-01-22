# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["FunctionImageto3dParams"]


class FunctionImageto3dParams(TypedDict, total=False):
    image_request_id: Required[Annotated[str, PropertyInfo(alias="imageRequestId")]]
    """The requestId from the /assets/create endpoint that the image was uploaded to"""

    seed: float
    """Seed used to generate the 3D model"""

    texture_size: Annotated[float, PropertyInfo(alias="textureSize")]
    """Size of the texture to use for the model.

    Higher values will result in more detailed models but will take longer to
    process. Must be one of 256, 512, 1024, 2048
    """
