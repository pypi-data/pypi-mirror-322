# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ComponentTextureObjectParams"]


class ComponentTextureObjectParams(TypedDict, total=False):
    mesh_request_id: Required[Annotated[str, PropertyInfo(alias="meshRequestId")]]
    """The requestId from the /assets/create endpoint that the model was uploaded to"""

    prompt_pos: Required[Annotated[str, PropertyInfo(alias="promptPos")]]
    """The positive prompt to use to describe the textures"""

    prompt_neg: Annotated[str, PropertyInfo(alias="promptNeg")]
    """The negative prompt to use to describe the textures.

    default is 'deformed, ugly, blurred'
    """

    seed: float
    """The seed to use for the generation (default is 1)"""
