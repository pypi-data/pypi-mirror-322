# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["FunctionCreateAnimalParams"]


class FunctionCreateAnimalParams(TypedDict, total=False):
    is_creative: Required[Annotated[bool, PropertyInfo(alias="isCreative")]]
    """Whether to use a creative approach for the generation.

    If true, the function will use the base_mesh_gen component to generate a more
    creative mesh. If false, the function will use the base_mesh_select component to
    generate a more conservative mesh.
    """

    mesh_prompt: Required[Annotated[str, PropertyInfo(alias="meshPrompt")]]
    """The prompt to use for the generation of the mesh"""

    mesh_variability: Required[Annotated[float, PropertyInfo(alias="meshVariability")]]
    """The variability of the mesh to use for the generation"""

    paint_prompt_neg: Required[Annotated[str, PropertyInfo(alias="paintPromptNeg")]]
    """The negative prompt to use to describe the textures"""

    paint_prompt_pos: Required[Annotated[str, PropertyInfo(alias="paintPromptPos")]]
    """The positive prompt to use to describe the textures"""
