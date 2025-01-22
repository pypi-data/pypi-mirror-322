# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ComponentBaseMeshGenParams"]


class ComponentBaseMeshGenParams(TypedDict, total=False):
    category: Required[str]
    """The category of the mesh to use for the generation.

    One or two words that describe the mesh. eg. 'sports ball', 'chair', 'table'
    """

    mesh_type: Required[Annotated[str, PropertyInfo(alias="meshType")]]
    """The type of mesh to use for the generation.

    Allowed values are (object, animal, humanoid)
    """

    mesh_variability: Required[Annotated[float, PropertyInfo(alias="meshVariability")]]
    """The variability of the mesh to use for the generation"""

    text_prompt: Required[Annotated[str, PropertyInfo(alias="textPrompt")]]
    """The prompt to use for the generation of the mesh.

    can be an empty string if imageRequestId is provided.
    """

    image_request_id: Annotated[str, PropertyInfo(alias="imageRequestId")]
    """The requestId from the /assets/create endpoint that the image was uploaded to"""
