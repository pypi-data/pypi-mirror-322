# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ComponentAnimateParams"]


class ComponentAnimateParams(TypedDict, total=False):
    moves_like_prompt: Required[Annotated[str, PropertyInfo(alias="movesLikePrompt")]]
    """The prompt to use to describe the animation"""

    seed: float
    """The seed to use for the generation (default is 1)"""
