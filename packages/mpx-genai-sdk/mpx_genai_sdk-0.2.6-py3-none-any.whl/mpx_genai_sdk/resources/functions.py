# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import (
    function_imageto3d_params,
    function_animate_human_params,
    function_create_animal_params,
    function_create_object_params,
    function_create_general_params,
)
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.shared.generate_response_object import GenerateResponseObject

__all__ = ["FunctionsResource", "AsyncFunctionsResource"]


class FunctionsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> FunctionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/masterpiecevr/mpx-sdk-python#accessing-raw-response-data-eg-headers
        """
        return FunctionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> FunctionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/masterpiecevr/mpx-sdk-python#with_streaming_response
        """
        return FunctionsResourceWithStreamingResponse(self)

    def animate_human(
        self,
        *,
        is_creative: bool,
        mesh_prompt: str,
        mesh_variability: float,
        paint_prompt_neg: str,
        paint_prompt_pos: str,
        animation_prompt: str | NotGiven = NOT_GIVEN,
        animation_type: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GenerateResponseObject:
        """
        This function generates a **Humanoid character** from the prompt descriptions.
        Once you make this function request, make note of the returned requestId. Then
        call the status endpoint to get the current status of the request. Currently,
        requests can take \\~~2-5mins to complete. You can optionally include animation
        capabilities to your character by setting the animationType to one of the
        following:

        - 'none' the model returned is a painted mesh only (like objects or animals)
        - 'rig_only' The model will be returned rigged and skinned in T-pose with no
          animation.
        - 'animate' returns a rigged and animated character.

        Note that if the animationType is not set to one of the above, it will default
        to 'none'.

        Args:
          is_creative: Whether to use a creative approach for the generation. If true, the function
              will use the base_mesh_gen component to generate a more creative mesh. If false,
              the function will use the base_mesh_select component to generate a more
              conservative mesh.

          mesh_prompt: The prompt to use for the generation of the mesh

          mesh_variability: The variability of the mesh to use for the generation

          paint_prompt_neg: The negative prompt to use to describe the textures

          paint_prompt_pos: The positive prompt to use to describe the textures

          animation_prompt: The prompt to use for the animation if animationType is set to **animate**.

          animation_type: The type of animation to use for the character. Allowed values are (none,
              rig_only, animate)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/functions/human",
            body=maybe_transform(
                {
                    "is_creative": is_creative,
                    "mesh_prompt": mesh_prompt,
                    "mesh_variability": mesh_variability,
                    "paint_prompt_neg": paint_prompt_neg,
                    "paint_prompt_pos": paint_prompt_pos,
                    "animation_prompt": animation_prompt,
                    "animation_type": animation_type,
                },
                function_animate_human_params.FunctionAnimateHumanParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenerateResponseObject,
        )

    def create_animal(
        self,
        *,
        is_creative: bool,
        mesh_prompt: str,
        mesh_variability: float,
        paint_prompt_neg: str,
        paint_prompt_pos: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GenerateResponseObject:
        """This function generates an **Animal** from the prompt descriptions.

        Once you
        make this function request, make note of the returned requestId. Then call the
        status endpoint to get the current status of the request. Currently, requests
        can take \\~~2-5mins to complete.

        Args:
          is_creative: Whether to use a creative approach for the generation. If true, the function
              will use the base_mesh_gen component to generate a more creative mesh. If false,
              the function will use the base_mesh_select component to generate a more
              conservative mesh.

          mesh_prompt: The prompt to use for the generation of the mesh

          mesh_variability: The variability of the mesh to use for the generation

          paint_prompt_neg: The negative prompt to use to describe the textures

          paint_prompt_pos: The positive prompt to use to describe the textures

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/functions/animal",
            body=maybe_transform(
                {
                    "is_creative": is_creative,
                    "mesh_prompt": mesh_prompt,
                    "mesh_variability": mesh_variability,
                    "paint_prompt_neg": paint_prompt_neg,
                    "paint_prompt_pos": paint_prompt_pos,
                },
                function_create_animal_params.FunctionCreateAnimalParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenerateResponseObject,
        )

    def create_general(
        self,
        *,
        prompt: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GenerateResponseObject:
        """
        This function generates anything from just a single prompt! Once you make this
        function request, make note of the returned requestId. Then call the status
        endpoint to get the current status of the request. Currently, requests can take
        \\~~2-5mins to complete.

        Args:
          prompt: The prompt to use for the generation

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/functions/general",
            body=maybe_transform({"prompt": prompt}, function_create_general_params.FunctionCreateGeneralParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenerateResponseObject,
        )

    def create_object(
        self,
        *,
        is_creative: bool,
        mesh_prompt: str,
        mesh_variability: float,
        paint_prompt_neg: str,
        paint_prompt_pos: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GenerateResponseObject:
        """This function generates an **Object** from the prompt descriptions.

        Once you
        make this function request, make note of the returned requestId. Then call the
        status endpoint to get the current status of the request. Currently, requests
        can take \\~~2-5mins to complete.

        Args:
          is_creative: Whether to use a creative approach for the generation. If true, the function
              will use the base_mesh_gen component to generate a more creative mesh. If false,
              the function will use the base_mesh_select component to generate a more
              conservative mesh.

          mesh_prompt: The prompt to use for the generation of the mesh

          mesh_variability: The variability of the mesh to use for the generation

          paint_prompt_neg: The negative prompt to use to describe the textures

          paint_prompt_pos: The positive prompt to use to describe the textures

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/functions/object",
            body=maybe_transform(
                {
                    "is_creative": is_creative,
                    "mesh_prompt": mesh_prompt,
                    "mesh_variability": mesh_variability,
                    "paint_prompt_neg": paint_prompt_neg,
                    "paint_prompt_pos": paint_prompt_pos,
                },
                function_create_object_params.FunctionCreateObjectParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenerateResponseObject,
        )

    def imageto3d(
        self,
        *,
        image_request_id: str,
        seed: float | NotGiven = NOT_GIVEN,
        texture_size: float | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GenerateResponseObject:
        """This function generates a 3D model (GLB, FBX, USDZ) from an image.

        To use the
        imageto3d endpoint, first call the **assets/create** endpoint to create an
        assetId for the image, then upload the image to our servers using the returned
        URL. Once you make this function request, make note of the returned requestId.
        Then call the status endpoint to get the current status of the request.
        Currently, requests can take \\~~1-2mins to complete.

        Args:
          image_request_id: The requestId from the /assets/create endpoint that the image was uploaded to

          seed: Seed used to generate the 3D model

          texture_size: Size of the texture to use for the model. Higher values will result in more
              detailed models but will take longer to process. Must be one of 256, 512, 1024,
              2048

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/functions/imageto3d",
            body=maybe_transform(
                {
                    "image_request_id": image_request_id,
                    "seed": seed,
                    "texture_size": texture_size,
                },
                function_imageto3d_params.FunctionImageto3dParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenerateResponseObject,
        )


class AsyncFunctionsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncFunctionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/masterpiecevr/mpx-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncFunctionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncFunctionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/masterpiecevr/mpx-sdk-python#with_streaming_response
        """
        return AsyncFunctionsResourceWithStreamingResponse(self)

    async def animate_human(
        self,
        *,
        is_creative: bool,
        mesh_prompt: str,
        mesh_variability: float,
        paint_prompt_neg: str,
        paint_prompt_pos: str,
        animation_prompt: str | NotGiven = NOT_GIVEN,
        animation_type: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GenerateResponseObject:
        """
        This function generates a **Humanoid character** from the prompt descriptions.
        Once you make this function request, make note of the returned requestId. Then
        call the status endpoint to get the current status of the request. Currently,
        requests can take \\~~2-5mins to complete. You can optionally include animation
        capabilities to your character by setting the animationType to one of the
        following:

        - 'none' the model returned is a painted mesh only (like objects or animals)
        - 'rig_only' The model will be returned rigged and skinned in T-pose with no
          animation.
        - 'animate' returns a rigged and animated character.

        Note that if the animationType is not set to one of the above, it will default
        to 'none'.

        Args:
          is_creative: Whether to use a creative approach for the generation. If true, the function
              will use the base_mesh_gen component to generate a more creative mesh. If false,
              the function will use the base_mesh_select component to generate a more
              conservative mesh.

          mesh_prompt: The prompt to use for the generation of the mesh

          mesh_variability: The variability of the mesh to use for the generation

          paint_prompt_neg: The negative prompt to use to describe the textures

          paint_prompt_pos: The positive prompt to use to describe the textures

          animation_prompt: The prompt to use for the animation if animationType is set to **animate**.

          animation_type: The type of animation to use for the character. Allowed values are (none,
              rig_only, animate)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/functions/human",
            body=await async_maybe_transform(
                {
                    "is_creative": is_creative,
                    "mesh_prompt": mesh_prompt,
                    "mesh_variability": mesh_variability,
                    "paint_prompt_neg": paint_prompt_neg,
                    "paint_prompt_pos": paint_prompt_pos,
                    "animation_prompt": animation_prompt,
                    "animation_type": animation_type,
                },
                function_animate_human_params.FunctionAnimateHumanParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenerateResponseObject,
        )

    async def create_animal(
        self,
        *,
        is_creative: bool,
        mesh_prompt: str,
        mesh_variability: float,
        paint_prompt_neg: str,
        paint_prompt_pos: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GenerateResponseObject:
        """This function generates an **Animal** from the prompt descriptions.

        Once you
        make this function request, make note of the returned requestId. Then call the
        status endpoint to get the current status of the request. Currently, requests
        can take \\~~2-5mins to complete.

        Args:
          is_creative: Whether to use a creative approach for the generation. If true, the function
              will use the base_mesh_gen component to generate a more creative mesh. If false,
              the function will use the base_mesh_select component to generate a more
              conservative mesh.

          mesh_prompt: The prompt to use for the generation of the mesh

          mesh_variability: The variability of the mesh to use for the generation

          paint_prompt_neg: The negative prompt to use to describe the textures

          paint_prompt_pos: The positive prompt to use to describe the textures

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/functions/animal",
            body=await async_maybe_transform(
                {
                    "is_creative": is_creative,
                    "mesh_prompt": mesh_prompt,
                    "mesh_variability": mesh_variability,
                    "paint_prompt_neg": paint_prompt_neg,
                    "paint_prompt_pos": paint_prompt_pos,
                },
                function_create_animal_params.FunctionCreateAnimalParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenerateResponseObject,
        )

    async def create_general(
        self,
        *,
        prompt: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GenerateResponseObject:
        """
        This function generates anything from just a single prompt! Once you make this
        function request, make note of the returned requestId. Then call the status
        endpoint to get the current status of the request. Currently, requests can take
        \\~~2-5mins to complete.

        Args:
          prompt: The prompt to use for the generation

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/functions/general",
            body=await async_maybe_transform(
                {"prompt": prompt}, function_create_general_params.FunctionCreateGeneralParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenerateResponseObject,
        )

    async def create_object(
        self,
        *,
        is_creative: bool,
        mesh_prompt: str,
        mesh_variability: float,
        paint_prompt_neg: str,
        paint_prompt_pos: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GenerateResponseObject:
        """This function generates an **Object** from the prompt descriptions.

        Once you
        make this function request, make note of the returned requestId. Then call the
        status endpoint to get the current status of the request. Currently, requests
        can take \\~~2-5mins to complete.

        Args:
          is_creative: Whether to use a creative approach for the generation. If true, the function
              will use the base_mesh_gen component to generate a more creative mesh. If false,
              the function will use the base_mesh_select component to generate a more
              conservative mesh.

          mesh_prompt: The prompt to use for the generation of the mesh

          mesh_variability: The variability of the mesh to use for the generation

          paint_prompt_neg: The negative prompt to use to describe the textures

          paint_prompt_pos: The positive prompt to use to describe the textures

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/functions/object",
            body=await async_maybe_transform(
                {
                    "is_creative": is_creative,
                    "mesh_prompt": mesh_prompt,
                    "mesh_variability": mesh_variability,
                    "paint_prompt_neg": paint_prompt_neg,
                    "paint_prompt_pos": paint_prompt_pos,
                },
                function_create_object_params.FunctionCreateObjectParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenerateResponseObject,
        )

    async def imageto3d(
        self,
        *,
        image_request_id: str,
        seed: float | NotGiven = NOT_GIVEN,
        texture_size: float | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GenerateResponseObject:
        """This function generates a 3D model (GLB, FBX, USDZ) from an image.

        To use the
        imageto3d endpoint, first call the **assets/create** endpoint to create an
        assetId for the image, then upload the image to our servers using the returned
        URL. Once you make this function request, make note of the returned requestId.
        Then call the status endpoint to get the current status of the request.
        Currently, requests can take \\~~1-2mins to complete.

        Args:
          image_request_id: The requestId from the /assets/create endpoint that the image was uploaded to

          seed: Seed used to generate the 3D model

          texture_size: Size of the texture to use for the model. Higher values will result in more
              detailed models but will take longer to process. Must be one of 256, 512, 1024,
              2048

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/functions/imageto3d",
            body=await async_maybe_transform(
                {
                    "image_request_id": image_request_id,
                    "seed": seed,
                    "texture_size": texture_size,
                },
                function_imageto3d_params.FunctionImageto3dParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenerateResponseObject,
        )


class FunctionsResourceWithRawResponse:
    def __init__(self, functions: FunctionsResource) -> None:
        self._functions = functions

        self.animate_human = to_raw_response_wrapper(
            functions.animate_human,
        )
        self.create_animal = to_raw_response_wrapper(
            functions.create_animal,
        )
        self.create_general = to_raw_response_wrapper(
            functions.create_general,
        )
        self.create_object = to_raw_response_wrapper(
            functions.create_object,
        )
        self.imageto3d = to_raw_response_wrapper(
            functions.imageto3d,
        )


class AsyncFunctionsResourceWithRawResponse:
    def __init__(self, functions: AsyncFunctionsResource) -> None:
        self._functions = functions

        self.animate_human = async_to_raw_response_wrapper(
            functions.animate_human,
        )
        self.create_animal = async_to_raw_response_wrapper(
            functions.create_animal,
        )
        self.create_general = async_to_raw_response_wrapper(
            functions.create_general,
        )
        self.create_object = async_to_raw_response_wrapper(
            functions.create_object,
        )
        self.imageto3d = async_to_raw_response_wrapper(
            functions.imageto3d,
        )


class FunctionsResourceWithStreamingResponse:
    def __init__(self, functions: FunctionsResource) -> None:
        self._functions = functions

        self.animate_human = to_streamed_response_wrapper(
            functions.animate_human,
        )
        self.create_animal = to_streamed_response_wrapper(
            functions.create_animal,
        )
        self.create_general = to_streamed_response_wrapper(
            functions.create_general,
        )
        self.create_object = to_streamed_response_wrapper(
            functions.create_object,
        )
        self.imageto3d = to_streamed_response_wrapper(
            functions.imageto3d,
        )


class AsyncFunctionsResourceWithStreamingResponse:
    def __init__(self, functions: AsyncFunctionsResource) -> None:
        self._functions = functions

        self.animate_human = async_to_streamed_response_wrapper(
            functions.animate_human,
        )
        self.create_animal = async_to_streamed_response_wrapper(
            functions.create_animal,
        )
        self.create_general = async_to_streamed_response_wrapper(
            functions.create_general,
        )
        self.create_object = async_to_streamed_response_wrapper(
            functions.create_object,
        )
        self.imageto3d = async_to_streamed_response_wrapper(
            functions.imageto3d,
        )
