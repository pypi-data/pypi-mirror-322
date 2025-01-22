# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from mpx_genai_sdk import Masterpiecex, AsyncMasterpiecex
from mpx_genai_sdk.types.shared import CreateResponseObject, GenerateResponseObject

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestComponents:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_animate(self, client: Masterpiecex) -> None:
        component = client.components.animate(
            moves_like_prompt="walking in circles",
        )
        assert_matches_type(GenerateResponseObject, component, path=["response"])

    @parametrize
    def test_method_animate_with_all_params(self, client: Masterpiecex) -> None:
        component = client.components.animate(
            moves_like_prompt="walking in circles",
            seed=2,
        )
        assert_matches_type(GenerateResponseObject, component, path=["response"])

    @parametrize
    def test_raw_response_animate(self, client: Masterpiecex) -> None:
        response = client.components.with_raw_response.animate(
            moves_like_prompt="walking in circles",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        component = response.parse()
        assert_matches_type(GenerateResponseObject, component, path=["response"])

    @parametrize
    def test_streaming_response_animate(self, client: Masterpiecex) -> None:
        with client.components.with_streaming_response.animate(
            moves_like_prompt="walking in circles",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            component = response.parse()
            assert_matches_type(GenerateResponseObject, component, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_base_mesh_gen(self, client: Masterpiecex) -> None:
        component = client.components.base_mesh_gen(
            category="category",
            mesh_type="meshType",
            mesh_variability=0,
            text_prompt="textPrompt",
        )
        assert_matches_type(GenerateResponseObject, component, path=["response"])

    @parametrize
    def test_method_base_mesh_gen_with_all_params(self, client: Masterpiecex) -> None:
        component = client.components.base_mesh_gen(
            category="category",
            mesh_type="meshType",
            mesh_variability=0,
            text_prompt="textPrompt",
            image_request_id="imageRequestId",
        )
        assert_matches_type(GenerateResponseObject, component, path=["response"])

    @parametrize
    def test_raw_response_base_mesh_gen(self, client: Masterpiecex) -> None:
        response = client.components.with_raw_response.base_mesh_gen(
            category="category",
            mesh_type="meshType",
            mesh_variability=0,
            text_prompt="textPrompt",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        component = response.parse()
        assert_matches_type(GenerateResponseObject, component, path=["response"])

    @parametrize
    def test_streaming_response_base_mesh_gen(self, client: Masterpiecex) -> None:
        with client.components.with_streaming_response.base_mesh_gen(
            category="category",
            mesh_type="meshType",
            mesh_variability=0,
            text_prompt="textPrompt",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            component = response.parse()
            assert_matches_type(GenerateResponseObject, component, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_base_mesh_select(self, client: Masterpiecex) -> None:
        component = client.components.base_mesh_select(
            category="sports ball",
            mesh_type="object",
            mesh_variability=2,
            text_prompt="basketball",
        )
        assert_matches_type(GenerateResponseObject, component, path=["response"])

    @parametrize
    def test_raw_response_base_mesh_select(self, client: Masterpiecex) -> None:
        response = client.components.with_raw_response.base_mesh_select(
            category="sports ball",
            mesh_type="object",
            mesh_variability=2,
            text_prompt="basketball",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        component = response.parse()
        assert_matches_type(GenerateResponseObject, component, path=["response"])

    @parametrize
    def test_streaming_response_base_mesh_select(self, client: Masterpiecex) -> None:
        with client.components.with_streaming_response.base_mesh_select(
            category="sports ball",
            mesh_type="object",
            mesh_variability=2,
            text_prompt="basketball",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            component = response.parse()
            assert_matches_type(GenerateResponseObject, component, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_generate_glb(self, client: Masterpiecex) -> None:
        component = client.components.generate_glb(
            mesh_request_id="xxxxxxx",
            mesh_type="object",
            texture_request_id="xxxxxxx",
        )
        assert_matches_type(GenerateResponseObject, component, path=["response"])

    @parametrize
    def test_method_generate_glb_with_all_params(self, client: Masterpiecex) -> None:
        component = client.components.generate_glb(
            mesh_request_id="xxxxxxx",
            mesh_type="object",
            texture_request_id="xxxxxxx",
            animation_request_id="xxxxxxx",
            rig_only=False,
        )
        assert_matches_type(GenerateResponseObject, component, path=["response"])

    @parametrize
    def test_raw_response_generate_glb(self, client: Masterpiecex) -> None:
        response = client.components.with_raw_response.generate_glb(
            mesh_request_id="xxxxxxx",
            mesh_type="object",
            texture_request_id="xxxxxxx",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        component = response.parse()
        assert_matches_type(GenerateResponseObject, component, path=["response"])

    @parametrize
    def test_streaming_response_generate_glb(self, client: Masterpiecex) -> None:
        with client.components.with_streaming_response.generate_glb(
            mesh_request_id="xxxxxxx",
            mesh_type="object",
            texture_request_id="xxxxxxx",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            component = response.parse()
            assert_matches_type(GenerateResponseObject, component, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_optimize(self, client: Masterpiecex) -> None:
        component = client.components.optimize(
            asset_request_id="xxxxxxx",
            object_type="humanoid",
            output_file_format="FBX",
            target_ratio=0.5,
        )
        assert_matches_type(CreateResponseObject, component, path=["response"])

    @parametrize
    def test_raw_response_optimize(self, client: Masterpiecex) -> None:
        response = client.components.with_raw_response.optimize(
            asset_request_id="xxxxxxx",
            object_type="humanoid",
            output_file_format="FBX",
            target_ratio=0.5,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        component = response.parse()
        assert_matches_type(CreateResponseObject, component, path=["response"])

    @parametrize
    def test_streaming_response_optimize(self, client: Masterpiecex) -> None:
        with client.components.with_streaming_response.optimize(
            asset_request_id="xxxxxxx",
            object_type="humanoid",
            output_file_format="FBX",
            target_ratio=0.5,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            component = response.parse()
            assert_matches_type(CreateResponseObject, component, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_texture_animals_humanoids(self, client: Masterpiecex) -> None:
        component = client.components.texture_animals_humanoids(
            mesh_request_id="xxxxxxx",
            prompt_pos="red ball with yellow stripes. Mat finish with small bumps",
        )
        assert_matches_type(GenerateResponseObject, component, path=["response"])

    @parametrize
    def test_method_texture_animals_humanoids_with_all_params(self, client: Masterpiecex) -> None:
        component = client.components.texture_animals_humanoids(
            mesh_request_id="xxxxxxx",
            prompt_pos="red ball with yellow stripes. Mat finish with small bumps",
            prompt_neg="blurry, low quality, low res, pixel",
            seed=2,
        )
        assert_matches_type(GenerateResponseObject, component, path=["response"])

    @parametrize
    def test_raw_response_texture_animals_humanoids(self, client: Masterpiecex) -> None:
        response = client.components.with_raw_response.texture_animals_humanoids(
            mesh_request_id="xxxxxxx",
            prompt_pos="red ball with yellow stripes. Mat finish with small bumps",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        component = response.parse()
        assert_matches_type(GenerateResponseObject, component, path=["response"])

    @parametrize
    def test_streaming_response_texture_animals_humanoids(self, client: Masterpiecex) -> None:
        with client.components.with_streaming_response.texture_animals_humanoids(
            mesh_request_id="xxxxxxx",
            prompt_pos="red ball with yellow stripes. Mat finish with small bumps",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            component = response.parse()
            assert_matches_type(GenerateResponseObject, component, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_texture_object(self, client: Masterpiecex) -> None:
        component = client.components.texture_object(
            mesh_request_id="xxxxxxx",
            prompt_pos="red ball with yellow stripes. Mat finish with small bumps",
        )
        assert_matches_type(GenerateResponseObject, component, path=["response"])

    @parametrize
    def test_method_texture_object_with_all_params(self, client: Masterpiecex) -> None:
        component = client.components.texture_object(
            mesh_request_id="xxxxxxx",
            prompt_pos="red ball with yellow stripes. Mat finish with small bumps",
            prompt_neg="blurry, low quality, low res, pixel",
            seed=2,
        )
        assert_matches_type(GenerateResponseObject, component, path=["response"])

    @parametrize
    def test_raw_response_texture_object(self, client: Masterpiecex) -> None:
        response = client.components.with_raw_response.texture_object(
            mesh_request_id="xxxxxxx",
            prompt_pos="red ball with yellow stripes. Mat finish with small bumps",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        component = response.parse()
        assert_matches_type(GenerateResponseObject, component, path=["response"])

    @parametrize
    def test_streaming_response_texture_object(self, client: Masterpiecex) -> None:
        with client.components.with_streaming_response.texture_object(
            mesh_request_id="xxxxxxx",
            prompt_pos="red ball with yellow stripes. Mat finish with small bumps",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            component = response.parse()
            assert_matches_type(GenerateResponseObject, component, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncComponents:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_animate(self, async_client: AsyncMasterpiecex) -> None:
        component = await async_client.components.animate(
            moves_like_prompt="walking in circles",
        )
        assert_matches_type(GenerateResponseObject, component, path=["response"])

    @parametrize
    async def test_method_animate_with_all_params(self, async_client: AsyncMasterpiecex) -> None:
        component = await async_client.components.animate(
            moves_like_prompt="walking in circles",
            seed=2,
        )
        assert_matches_type(GenerateResponseObject, component, path=["response"])

    @parametrize
    async def test_raw_response_animate(self, async_client: AsyncMasterpiecex) -> None:
        response = await async_client.components.with_raw_response.animate(
            moves_like_prompt="walking in circles",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        component = await response.parse()
        assert_matches_type(GenerateResponseObject, component, path=["response"])

    @parametrize
    async def test_streaming_response_animate(self, async_client: AsyncMasterpiecex) -> None:
        async with async_client.components.with_streaming_response.animate(
            moves_like_prompt="walking in circles",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            component = await response.parse()
            assert_matches_type(GenerateResponseObject, component, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_base_mesh_gen(self, async_client: AsyncMasterpiecex) -> None:
        component = await async_client.components.base_mesh_gen(
            category="category",
            mesh_type="meshType",
            mesh_variability=0,
            text_prompt="textPrompt",
        )
        assert_matches_type(GenerateResponseObject, component, path=["response"])

    @parametrize
    async def test_method_base_mesh_gen_with_all_params(self, async_client: AsyncMasterpiecex) -> None:
        component = await async_client.components.base_mesh_gen(
            category="category",
            mesh_type="meshType",
            mesh_variability=0,
            text_prompt="textPrompt",
            image_request_id="imageRequestId",
        )
        assert_matches_type(GenerateResponseObject, component, path=["response"])

    @parametrize
    async def test_raw_response_base_mesh_gen(self, async_client: AsyncMasterpiecex) -> None:
        response = await async_client.components.with_raw_response.base_mesh_gen(
            category="category",
            mesh_type="meshType",
            mesh_variability=0,
            text_prompt="textPrompt",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        component = await response.parse()
        assert_matches_type(GenerateResponseObject, component, path=["response"])

    @parametrize
    async def test_streaming_response_base_mesh_gen(self, async_client: AsyncMasterpiecex) -> None:
        async with async_client.components.with_streaming_response.base_mesh_gen(
            category="category",
            mesh_type="meshType",
            mesh_variability=0,
            text_prompt="textPrompt",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            component = await response.parse()
            assert_matches_type(GenerateResponseObject, component, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_base_mesh_select(self, async_client: AsyncMasterpiecex) -> None:
        component = await async_client.components.base_mesh_select(
            category="sports ball",
            mesh_type="object",
            mesh_variability=2,
            text_prompt="basketball",
        )
        assert_matches_type(GenerateResponseObject, component, path=["response"])

    @parametrize
    async def test_raw_response_base_mesh_select(self, async_client: AsyncMasterpiecex) -> None:
        response = await async_client.components.with_raw_response.base_mesh_select(
            category="sports ball",
            mesh_type="object",
            mesh_variability=2,
            text_prompt="basketball",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        component = await response.parse()
        assert_matches_type(GenerateResponseObject, component, path=["response"])

    @parametrize
    async def test_streaming_response_base_mesh_select(self, async_client: AsyncMasterpiecex) -> None:
        async with async_client.components.with_streaming_response.base_mesh_select(
            category="sports ball",
            mesh_type="object",
            mesh_variability=2,
            text_prompt="basketball",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            component = await response.parse()
            assert_matches_type(GenerateResponseObject, component, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_generate_glb(self, async_client: AsyncMasterpiecex) -> None:
        component = await async_client.components.generate_glb(
            mesh_request_id="xxxxxxx",
            mesh_type="object",
            texture_request_id="xxxxxxx",
        )
        assert_matches_type(GenerateResponseObject, component, path=["response"])

    @parametrize
    async def test_method_generate_glb_with_all_params(self, async_client: AsyncMasterpiecex) -> None:
        component = await async_client.components.generate_glb(
            mesh_request_id="xxxxxxx",
            mesh_type="object",
            texture_request_id="xxxxxxx",
            animation_request_id="xxxxxxx",
            rig_only=False,
        )
        assert_matches_type(GenerateResponseObject, component, path=["response"])

    @parametrize
    async def test_raw_response_generate_glb(self, async_client: AsyncMasterpiecex) -> None:
        response = await async_client.components.with_raw_response.generate_glb(
            mesh_request_id="xxxxxxx",
            mesh_type="object",
            texture_request_id="xxxxxxx",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        component = await response.parse()
        assert_matches_type(GenerateResponseObject, component, path=["response"])

    @parametrize
    async def test_streaming_response_generate_glb(self, async_client: AsyncMasterpiecex) -> None:
        async with async_client.components.with_streaming_response.generate_glb(
            mesh_request_id="xxxxxxx",
            mesh_type="object",
            texture_request_id="xxxxxxx",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            component = await response.parse()
            assert_matches_type(GenerateResponseObject, component, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_optimize(self, async_client: AsyncMasterpiecex) -> None:
        component = await async_client.components.optimize(
            asset_request_id="xxxxxxx",
            object_type="humanoid",
            output_file_format="FBX",
            target_ratio=0.5,
        )
        assert_matches_type(CreateResponseObject, component, path=["response"])

    @parametrize
    async def test_raw_response_optimize(self, async_client: AsyncMasterpiecex) -> None:
        response = await async_client.components.with_raw_response.optimize(
            asset_request_id="xxxxxxx",
            object_type="humanoid",
            output_file_format="FBX",
            target_ratio=0.5,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        component = await response.parse()
        assert_matches_type(CreateResponseObject, component, path=["response"])

    @parametrize
    async def test_streaming_response_optimize(self, async_client: AsyncMasterpiecex) -> None:
        async with async_client.components.with_streaming_response.optimize(
            asset_request_id="xxxxxxx",
            object_type="humanoid",
            output_file_format="FBX",
            target_ratio=0.5,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            component = await response.parse()
            assert_matches_type(CreateResponseObject, component, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_texture_animals_humanoids(self, async_client: AsyncMasterpiecex) -> None:
        component = await async_client.components.texture_animals_humanoids(
            mesh_request_id="xxxxxxx",
            prompt_pos="red ball with yellow stripes. Mat finish with small bumps",
        )
        assert_matches_type(GenerateResponseObject, component, path=["response"])

    @parametrize
    async def test_method_texture_animals_humanoids_with_all_params(self, async_client: AsyncMasterpiecex) -> None:
        component = await async_client.components.texture_animals_humanoids(
            mesh_request_id="xxxxxxx",
            prompt_pos="red ball with yellow stripes. Mat finish with small bumps",
            prompt_neg="blurry, low quality, low res, pixel",
            seed=2,
        )
        assert_matches_type(GenerateResponseObject, component, path=["response"])

    @parametrize
    async def test_raw_response_texture_animals_humanoids(self, async_client: AsyncMasterpiecex) -> None:
        response = await async_client.components.with_raw_response.texture_animals_humanoids(
            mesh_request_id="xxxxxxx",
            prompt_pos="red ball with yellow stripes. Mat finish with small bumps",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        component = await response.parse()
        assert_matches_type(GenerateResponseObject, component, path=["response"])

    @parametrize
    async def test_streaming_response_texture_animals_humanoids(self, async_client: AsyncMasterpiecex) -> None:
        async with async_client.components.with_streaming_response.texture_animals_humanoids(
            mesh_request_id="xxxxxxx",
            prompt_pos="red ball with yellow stripes. Mat finish with small bumps",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            component = await response.parse()
            assert_matches_type(GenerateResponseObject, component, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_texture_object(self, async_client: AsyncMasterpiecex) -> None:
        component = await async_client.components.texture_object(
            mesh_request_id="xxxxxxx",
            prompt_pos="red ball with yellow stripes. Mat finish with small bumps",
        )
        assert_matches_type(GenerateResponseObject, component, path=["response"])

    @parametrize
    async def test_method_texture_object_with_all_params(self, async_client: AsyncMasterpiecex) -> None:
        component = await async_client.components.texture_object(
            mesh_request_id="xxxxxxx",
            prompt_pos="red ball with yellow stripes. Mat finish with small bumps",
            prompt_neg="blurry, low quality, low res, pixel",
            seed=2,
        )
        assert_matches_type(GenerateResponseObject, component, path=["response"])

    @parametrize
    async def test_raw_response_texture_object(self, async_client: AsyncMasterpiecex) -> None:
        response = await async_client.components.with_raw_response.texture_object(
            mesh_request_id="xxxxxxx",
            prompt_pos="red ball with yellow stripes. Mat finish with small bumps",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        component = await response.parse()
        assert_matches_type(GenerateResponseObject, component, path=["response"])

    @parametrize
    async def test_streaming_response_texture_object(self, async_client: AsyncMasterpiecex) -> None:
        async with async_client.components.with_streaming_response.texture_object(
            mesh_request_id="xxxxxxx",
            prompt_pos="red ball with yellow stripes. Mat finish with small bumps",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            component = await response.parse()
            assert_matches_type(GenerateResponseObject, component, path=["response"])

        assert cast(Any, response.is_closed) is True
