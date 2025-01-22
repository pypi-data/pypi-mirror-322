# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from mpx_genai_sdk import Masterpiecex, AsyncMasterpiecex
from mpx_genai_sdk.types.shared import GenerateResponseObject

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestFunctions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_animate_human(self, client: Masterpiecex) -> None:
        function = client.functions.animate_human(
            is_creative=True,
            mesh_prompt="meshPrompt",
            mesh_variability=2,
            paint_prompt_neg="paintPromptNeg",
            paint_prompt_pos="paintPromptPos",
        )
        assert_matches_type(GenerateResponseObject, function, path=["response"])

    @parametrize
    def test_method_animate_human_with_all_params(self, client: Masterpiecex) -> None:
        function = client.functions.animate_human(
            is_creative=True,
            mesh_prompt="meshPrompt",
            mesh_variability=2,
            paint_prompt_neg="paintPromptNeg",
            paint_prompt_pos="paintPromptPos",
            animation_prompt="walking in circles",
            animation_type="animationType",
        )
        assert_matches_type(GenerateResponseObject, function, path=["response"])

    @parametrize
    def test_raw_response_animate_human(self, client: Masterpiecex) -> None:
        response = client.functions.with_raw_response.animate_human(
            is_creative=True,
            mesh_prompt="meshPrompt",
            mesh_variability=2,
            paint_prompt_neg="paintPromptNeg",
            paint_prompt_pos="paintPromptPos",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        function = response.parse()
        assert_matches_type(GenerateResponseObject, function, path=["response"])

    @parametrize
    def test_streaming_response_animate_human(self, client: Masterpiecex) -> None:
        with client.functions.with_streaming_response.animate_human(
            is_creative=True,
            mesh_prompt="meshPrompt",
            mesh_variability=2,
            paint_prompt_neg="paintPromptNeg",
            paint_prompt_pos="paintPromptPos",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            function = response.parse()
            assert_matches_type(GenerateResponseObject, function, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_create_animal(self, client: Masterpiecex) -> None:
        function = client.functions.create_animal(
            is_creative=False,
            mesh_prompt="bird",
            mesh_variability=2,
            paint_prompt_neg="blurry, low quality, low res, pixel",
            paint_prompt_pos="Bird, bluejay, hyperrealistic, Highly Detailed",
        )
        assert_matches_type(GenerateResponseObject, function, path=["response"])

    @parametrize
    def test_raw_response_create_animal(self, client: Masterpiecex) -> None:
        response = client.functions.with_raw_response.create_animal(
            is_creative=False,
            mesh_prompt="bird",
            mesh_variability=2,
            paint_prompt_neg="blurry, low quality, low res, pixel",
            paint_prompt_pos="Bird, bluejay, hyperrealistic, Highly Detailed",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        function = response.parse()
        assert_matches_type(GenerateResponseObject, function, path=["response"])

    @parametrize
    def test_streaming_response_create_animal(self, client: Masterpiecex) -> None:
        with client.functions.with_streaming_response.create_animal(
            is_creative=False,
            mesh_prompt="bird",
            mesh_variability=2,
            paint_prompt_neg="blurry, low quality, low res, pixel",
            paint_prompt_pos="Bird, bluejay, hyperrealistic, Highly Detailed",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            function = response.parse()
            assert_matches_type(GenerateResponseObject, function, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_create_general(self, client: Masterpiecex) -> None:
        function = client.functions.create_general(
            prompt="cute dog",
        )
        assert_matches_type(GenerateResponseObject, function, path=["response"])

    @parametrize
    def test_raw_response_create_general(self, client: Masterpiecex) -> None:
        response = client.functions.with_raw_response.create_general(
            prompt="cute dog",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        function = response.parse()
        assert_matches_type(GenerateResponseObject, function, path=["response"])

    @parametrize
    def test_streaming_response_create_general(self, client: Masterpiecex) -> None:
        with client.functions.with_streaming_response.create_general(
            prompt="cute dog",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            function = response.parse()
            assert_matches_type(GenerateResponseObject, function, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_create_object(self, client: Masterpiecex) -> None:
        function = client.functions.create_object(
            is_creative=True,
            mesh_prompt="piano, musical instrument",
            mesh_variability=2,
            paint_prompt_neg="blurry, low quality, low res, pixel",
            paint_prompt_pos="piano, musical instrument, Exquisite grand piano, ebony black with ivory keys, shiny, classic",
        )
        assert_matches_type(GenerateResponseObject, function, path=["response"])

    @parametrize
    def test_raw_response_create_object(self, client: Masterpiecex) -> None:
        response = client.functions.with_raw_response.create_object(
            is_creative=True,
            mesh_prompt="piano, musical instrument",
            mesh_variability=2,
            paint_prompt_neg="blurry, low quality, low res, pixel",
            paint_prompt_pos="piano, musical instrument, Exquisite grand piano, ebony black with ivory keys, shiny, classic",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        function = response.parse()
        assert_matches_type(GenerateResponseObject, function, path=["response"])

    @parametrize
    def test_streaming_response_create_object(self, client: Masterpiecex) -> None:
        with client.functions.with_streaming_response.create_object(
            is_creative=True,
            mesh_prompt="piano, musical instrument",
            mesh_variability=2,
            paint_prompt_neg="blurry, low quality, low res, pixel",
            paint_prompt_pos="piano, musical instrument, Exquisite grand piano, ebony black with ivory keys, shiny, classic",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            function = response.parse()
            assert_matches_type(GenerateResponseObject, function, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_imageto3d(self, client: Masterpiecex) -> None:
        function = client.functions.imageto3d(
            image_request_id="<requestId from /assets/create>",
        )
        assert_matches_type(GenerateResponseObject, function, path=["response"])

    @parametrize
    def test_method_imageto3d_with_all_params(self, client: Masterpiecex) -> None:
        function = client.functions.imageto3d(
            image_request_id="<requestId from /assets/create>",
            seed=0,
            texture_size=0,
        )
        assert_matches_type(GenerateResponseObject, function, path=["response"])

    @parametrize
    def test_raw_response_imageto3d(self, client: Masterpiecex) -> None:
        response = client.functions.with_raw_response.imageto3d(
            image_request_id="<requestId from /assets/create>",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        function = response.parse()
        assert_matches_type(GenerateResponseObject, function, path=["response"])

    @parametrize
    def test_streaming_response_imageto3d(self, client: Masterpiecex) -> None:
        with client.functions.with_streaming_response.imageto3d(
            image_request_id="<requestId from /assets/create>",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            function = response.parse()
            assert_matches_type(GenerateResponseObject, function, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncFunctions:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_animate_human(self, async_client: AsyncMasterpiecex) -> None:
        function = await async_client.functions.animate_human(
            is_creative=True,
            mesh_prompt="meshPrompt",
            mesh_variability=2,
            paint_prompt_neg="paintPromptNeg",
            paint_prompt_pos="paintPromptPos",
        )
        assert_matches_type(GenerateResponseObject, function, path=["response"])

    @parametrize
    async def test_method_animate_human_with_all_params(self, async_client: AsyncMasterpiecex) -> None:
        function = await async_client.functions.animate_human(
            is_creative=True,
            mesh_prompt="meshPrompt",
            mesh_variability=2,
            paint_prompt_neg="paintPromptNeg",
            paint_prompt_pos="paintPromptPos",
            animation_prompt="walking in circles",
            animation_type="animationType",
        )
        assert_matches_type(GenerateResponseObject, function, path=["response"])

    @parametrize
    async def test_raw_response_animate_human(self, async_client: AsyncMasterpiecex) -> None:
        response = await async_client.functions.with_raw_response.animate_human(
            is_creative=True,
            mesh_prompt="meshPrompt",
            mesh_variability=2,
            paint_prompt_neg="paintPromptNeg",
            paint_prompt_pos="paintPromptPos",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        function = await response.parse()
        assert_matches_type(GenerateResponseObject, function, path=["response"])

    @parametrize
    async def test_streaming_response_animate_human(self, async_client: AsyncMasterpiecex) -> None:
        async with async_client.functions.with_streaming_response.animate_human(
            is_creative=True,
            mesh_prompt="meshPrompt",
            mesh_variability=2,
            paint_prompt_neg="paintPromptNeg",
            paint_prompt_pos="paintPromptPos",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            function = await response.parse()
            assert_matches_type(GenerateResponseObject, function, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_create_animal(self, async_client: AsyncMasterpiecex) -> None:
        function = await async_client.functions.create_animal(
            is_creative=False,
            mesh_prompt="bird",
            mesh_variability=2,
            paint_prompt_neg="blurry, low quality, low res, pixel",
            paint_prompt_pos="Bird, bluejay, hyperrealistic, Highly Detailed",
        )
        assert_matches_type(GenerateResponseObject, function, path=["response"])

    @parametrize
    async def test_raw_response_create_animal(self, async_client: AsyncMasterpiecex) -> None:
        response = await async_client.functions.with_raw_response.create_animal(
            is_creative=False,
            mesh_prompt="bird",
            mesh_variability=2,
            paint_prompt_neg="blurry, low quality, low res, pixel",
            paint_prompt_pos="Bird, bluejay, hyperrealistic, Highly Detailed",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        function = await response.parse()
        assert_matches_type(GenerateResponseObject, function, path=["response"])

    @parametrize
    async def test_streaming_response_create_animal(self, async_client: AsyncMasterpiecex) -> None:
        async with async_client.functions.with_streaming_response.create_animal(
            is_creative=False,
            mesh_prompt="bird",
            mesh_variability=2,
            paint_prompt_neg="blurry, low quality, low res, pixel",
            paint_prompt_pos="Bird, bluejay, hyperrealistic, Highly Detailed",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            function = await response.parse()
            assert_matches_type(GenerateResponseObject, function, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_create_general(self, async_client: AsyncMasterpiecex) -> None:
        function = await async_client.functions.create_general(
            prompt="cute dog",
        )
        assert_matches_type(GenerateResponseObject, function, path=["response"])

    @parametrize
    async def test_raw_response_create_general(self, async_client: AsyncMasterpiecex) -> None:
        response = await async_client.functions.with_raw_response.create_general(
            prompt="cute dog",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        function = await response.parse()
        assert_matches_type(GenerateResponseObject, function, path=["response"])

    @parametrize
    async def test_streaming_response_create_general(self, async_client: AsyncMasterpiecex) -> None:
        async with async_client.functions.with_streaming_response.create_general(
            prompt="cute dog",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            function = await response.parse()
            assert_matches_type(GenerateResponseObject, function, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_create_object(self, async_client: AsyncMasterpiecex) -> None:
        function = await async_client.functions.create_object(
            is_creative=True,
            mesh_prompt="piano, musical instrument",
            mesh_variability=2,
            paint_prompt_neg="blurry, low quality, low res, pixel",
            paint_prompt_pos="piano, musical instrument, Exquisite grand piano, ebony black with ivory keys, shiny, classic",
        )
        assert_matches_type(GenerateResponseObject, function, path=["response"])

    @parametrize
    async def test_raw_response_create_object(self, async_client: AsyncMasterpiecex) -> None:
        response = await async_client.functions.with_raw_response.create_object(
            is_creative=True,
            mesh_prompt="piano, musical instrument",
            mesh_variability=2,
            paint_prompt_neg="blurry, low quality, low res, pixel",
            paint_prompt_pos="piano, musical instrument, Exquisite grand piano, ebony black with ivory keys, shiny, classic",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        function = await response.parse()
        assert_matches_type(GenerateResponseObject, function, path=["response"])

    @parametrize
    async def test_streaming_response_create_object(self, async_client: AsyncMasterpiecex) -> None:
        async with async_client.functions.with_streaming_response.create_object(
            is_creative=True,
            mesh_prompt="piano, musical instrument",
            mesh_variability=2,
            paint_prompt_neg="blurry, low quality, low res, pixel",
            paint_prompt_pos="piano, musical instrument, Exquisite grand piano, ebony black with ivory keys, shiny, classic",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            function = await response.parse()
            assert_matches_type(GenerateResponseObject, function, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_imageto3d(self, async_client: AsyncMasterpiecex) -> None:
        function = await async_client.functions.imageto3d(
            image_request_id="<requestId from /assets/create>",
        )
        assert_matches_type(GenerateResponseObject, function, path=["response"])

    @parametrize
    async def test_method_imageto3d_with_all_params(self, async_client: AsyncMasterpiecex) -> None:
        function = await async_client.functions.imageto3d(
            image_request_id="<requestId from /assets/create>",
            seed=0,
            texture_size=0,
        )
        assert_matches_type(GenerateResponseObject, function, path=["response"])

    @parametrize
    async def test_raw_response_imageto3d(self, async_client: AsyncMasterpiecex) -> None:
        response = await async_client.functions.with_raw_response.imageto3d(
            image_request_id="<requestId from /assets/create>",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        function = await response.parse()
        assert_matches_type(GenerateResponseObject, function, path=["response"])

    @parametrize
    async def test_streaming_response_imageto3d(self, async_client: AsyncMasterpiecex) -> None:
        async with async_client.functions.with_streaming_response.imageto3d(
            image_request_id="<requestId from /assets/create>",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            function = await response.parse()
            assert_matches_type(GenerateResponseObject, function, path=["response"])

        assert cast(Any, response.is_closed) is True
