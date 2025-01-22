# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ComponentGenerateGlbParams"]


class ComponentGenerateGlbParams(TypedDict, total=False):
    mesh_request_id: Required[Annotated[str, PropertyInfo(alias="meshRequestId")]]
    """The requestId from the /assets/create endpoint that the model was uploaded to"""

    mesh_type: Required[Annotated[str, PropertyInfo(alias="meshType")]]
    """The type of mesh to use for the generation.

    Allowed values are (object, animal, humanoid)
    """

    texture_request_id: Required[Annotated[str, PropertyInfo(alias="textureRequestId")]]
    """The requestId from the /assets/create endpoint that the texture was uploaded to"""

    animation_request_id: Annotated[str, PropertyInfo(alias="animationRequestId")]
    """
    The requestId from the /components/animate endpoint that the animation was
    uploaded to
    """

    rig_only: Annotated[bool, PropertyInfo(alias="rigOnly")]
    """Whether to return only a rigged and skinned model in T-pose with no animation.

    defaults to false. Note that not providing an animationRequestId and setting
    this to true will return a rigged and skinned model in T-pose with no animation.
    Not providing an animationRequestId and setting this to false will return a
    UV-ed model with no rigging or skinning. Providing an animationRequestId will
    override this setting and return a rigged and animated model.
    """
