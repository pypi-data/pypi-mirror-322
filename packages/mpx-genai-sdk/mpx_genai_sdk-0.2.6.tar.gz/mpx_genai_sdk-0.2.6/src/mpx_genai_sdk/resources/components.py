# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import (
    component_animate_params,
    component_optimize_params,
    component_generate_glb_params,
    component_base_mesh_gen_params,
    component_texture_object_params,
    component_base_mesh_select_params,
    component_texture_animals_humanoids_params,
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
from ..types.shared.create_response_object import CreateResponseObject
from ..types.shared.generate_response_object import GenerateResponseObject

__all__ = ["ComponentsResource", "AsyncComponentsResource"]


class ComponentsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ComponentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/masterpiecevr/mpx-sdk-python#accessing-raw-response-data-eg-headers
        """
        return ComponentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ComponentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/masterpiecevr/mpx-sdk-python#with_streaming_response
        """
        return ComponentsResourceWithStreamingResponse(self)

    def animate(
        self,
        *,
        moves_like_prompt: str,
        seed: float | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GenerateResponseObject:
        """
        This function creates a BVH animation file suitable for standard rigged
        humanoids. Use the status endpoint to check the status of the request. Save the
        returned requestId for use with other components as input.

        Args:
          moves_like_prompt: The prompt to use to describe the animation

          seed: The seed to use for the generation (default is 1)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/components/animate",
            body=maybe_transform(
                {
                    "moves_like_prompt": moves_like_prompt,
                    "seed": seed,
                },
                component_animate_params.ComponentAnimateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenerateResponseObject,
        )

    def base_mesh_gen(
        self,
        *,
        category: str,
        mesh_type: str,
        mesh_variability: float,
        text_prompt: str,
        image_request_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GenerateResponseObject:
        """
        This function uses a generative approach to create an OBJ model that you can use
        for further processing. It takes an image and/or a text as input and may create
        a more unique and creative model than the base mesh selector. You can supply an
        image and/or a text prompt as input. This component does not generate a UV map
        or textures. You can use the generated OBJ file as the base mesh for creating a
        thumbnail or as an input for texturing or animation. Use the status endpoint to
        check the status of the request. Save the returned requestId for use with other
        components as input.

        Args:
          category: The category of the mesh to use for the generation. One or two words that
              describe the mesh. eg. 'sports ball', 'chair', 'table'

          mesh_type: The type of mesh to use for the generation. Allowed values are (object, animal,
              humanoid)

          mesh_variability: The variability of the mesh to use for the generation

          text_prompt: The prompt to use for the generation of the mesh. can be an empty string if
              imageRequestId is provided.

          image_request_id: The requestId from the /assets/create endpoint that the image was uploaded to

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/components/base_mesh_gen",
            body=maybe_transform(
                {
                    "category": category,
                    "mesh_type": mesh_type,
                    "mesh_variability": mesh_variability,
                    "text_prompt": text_prompt,
                    "image_request_id": image_request_id,
                },
                component_base_mesh_gen_params.ComponentBaseMeshGenParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenerateResponseObject,
        )

    def base_mesh_select(
        self,
        *,
        category: str,
        mesh_type: str,
        mesh_variability: float,
        text_prompt: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GenerateResponseObject:
        """This function selects a model from a curated library using RAG.

        Use this
        function to select a conservative but high quality model for your project. This
        component does not generate a UV map or textures. It returns an OBJ file that
        you can use for further processing. You can use this OBJ file as the base mesh
        for creating a thumbnail or as an input for texturing or animation. Use the
        status endpoint to check the status of the request. Save the returned requestId
        for use with other components as input.

        Args:
          category: The category of the mesh to use for the generation. Allowed values are (object,
              animal, humanoid)

          mesh_type: The type of mesh to use for the generation. Allowed values are (object, animal,
              humanoid)

          mesh_variability: The variability of the mesh to use for the generation

          text_prompt: The prompt to use for the generation of the mesh

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/components/base_mesh_select",
            body=maybe_transform(
                {
                    "category": category,
                    "mesh_type": mesh_type,
                    "mesh_variability": mesh_variability,
                    "text_prompt": text_prompt,
                },
                component_base_mesh_select_params.ComponentBaseMeshSelectParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenerateResponseObject,
        )

    def generate_glb(
        self,
        *,
        mesh_request_id: str,
        mesh_type: str,
        texture_request_id: str,
        animation_request_id: str | NotGiven = NOT_GIVEN,
        rig_only: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GenerateResponseObject:
        """
        This function takes a UV'd OBJ model, a texture and optionally an animation and
        creates a GLB file that you can use for further processing. It also creates a
        thumbnail image, an FBX and USDZ file. Use the requestId from the
        **texture_object** endpoint for both the model and texture as input unless you
        are using an asset that has been uploaded. Use the requestId from the
        **animation** endpoint for the animation. Use the status endpoint to check the
        status of the request. Save the returned requestId for use with other components
        as input. Note that the outputUrl will be the URL of the GLB file. Other file
        types are available in the outputs object. Note that the **rigOnly** flag is
        optional and defaults to false. It only applies if the **meshType** is human. If
        set to true and the model is human, the model will be returned rigged and
        skinned in T-pose with no animation.

        Args:
          mesh_request_id: The requestId from the /assets/create endpoint that the model was uploaded to

          mesh_type: The type of mesh to use for the generation. Allowed values are (object, animal,
              humanoid)

          texture_request_id: The requestId from the /assets/create endpoint that the texture was uploaded to

          animation_request_id: The requestId from the /components/animate endpoint that the animation was
              uploaded to

          rig_only: Whether to return only a rigged and skinned model in T-pose with no animation.
              defaults to false. Note that not providing an animationRequestId and setting
              this to true will return a rigged and skinned model in T-pose with no animation.
              Not providing an animationRequestId and setting this to false will return a
              UV-ed model with no rigging or skinning. Providing an animationRequestId will
              override this setting and return a rigged and animated model.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/components/generate_glb",
            body=maybe_transform(
                {
                    "mesh_request_id": mesh_request_id,
                    "mesh_type": mesh_type,
                    "texture_request_id": texture_request_id,
                    "animation_request_id": animation_request_id,
                    "rig_only": rig_only,
                },
                component_generate_glb_params.ComponentGenerateGlbParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenerateResponseObject,
        )

    def optimize(
        self,
        *,
        asset_request_id: str,
        object_type: str,
        output_file_format: str,
        target_ratio: float,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CreateResponseObject:
        """
        This function optionally reduces the polycount of your model and/or returns a
        different file format. eg. convert from GLB to USDZ.

        The **assetRequestId** can be a requestId from a **Generate** request or an
        assetId from an **assets/create** request. If you are converting a model you
        uploaded, please ensure that the model has been uploaded before calling this
        endpoint.

        The **targetRatio** is the ratio of the original polycount that you want to
        reduce to. eg. 0.5 will reduce the polycount by 50%.

        The **outputFileFormat** is the file format you want the model returned in.
        Currently, we support FBX, GLB and USDZ.

        The **objectType** is the type of model you are uploading. Currently, we support
        'object', 'animal' and 'humanoid'.

        Args:
          asset_request_id: The requestId from the /assets/create endpoint that the model was uploaded to

          object_type: The type of model you are uploading. Currently, we support 'object', 'animal'
              and 'humanoid'.

          output_file_format: The file format you want the model returned in. Currently, we support FBX, GLB
              and USDZ.

          target_ratio: The ratio of the original polycount that you want to reduce to. eg. 0.5 will
              reduce the polycount by 50%.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/components/optimize",
            body=maybe_transform(
                {
                    "asset_request_id": asset_request_id,
                    "object_type": object_type,
                    "output_file_format": output_file_format,
                    "target_ratio": target_ratio,
                },
                component_optimize_params.ComponentOptimizeParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CreateResponseObject,
        )

    def texture_animals_humanoids(
        self,
        *,
        mesh_request_id: str,
        prompt_pos: str,
        prompt_neg: str | NotGiven = NOT_GIVEN,
        seed: float | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GenerateResponseObject:
        """
        This function creates a UV mapped version of the input OBJ model and generates a
        texture mapped png file. Use the requestId from the **base_mesh_select** or
        **mesh_gen** endpoint or an asset that has been uploaded as input. Use the seed
        to generate a different texture for the same model. Use this function to create
        a textured model from a base mesh or a generated mesh. It is primarily used for
        animals and humanoids. Use the status endpoint to check the status of the
        request. Save the returned requestId for use with other components as input.

        Args:
          mesh_request_id: The requestId from the /assets/create endpoint that the model was uploaded to

          prompt_pos: The positive prompt to use to describe the textures

          prompt_neg: The negative prompt to use to describe the textures. default is 'deformed, ugly,
              blurred'

          seed: The seed to use for the generation (default is 1)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/components/texture",
            body=maybe_transform(
                {
                    "mesh_request_id": mesh_request_id,
                    "prompt_pos": prompt_pos,
                    "prompt_neg": prompt_neg,
                    "seed": seed,
                },
                component_texture_animals_humanoids_params.ComponentTextureAnimalsHumanoidsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenerateResponseObject,
        )

    def texture_object(
        self,
        *,
        mesh_request_id: str,
        prompt_pos: str,
        prompt_neg: str | NotGiven = NOT_GIVEN,
        seed: float | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GenerateResponseObject:
        """
        This function creates a UV mapped version of the input OBJ model and generates a
        texture mapped png file. Use the requestId from the **base_mesh_select** or
        **mesh_gen** endpoint or an asset that has been uploaded as input. Use the seed
        to generate a different texture for the same model. Use this function to create
        a textured model from a base mesh or a generated mesh. It is primarily used for
        objects, not humanoids. Use the status endpoint to check the status of the
        request. Save the returned requestId for use with other components as input.

        Args:
          mesh_request_id: The requestId from the /assets/create endpoint that the model was uploaded to

          prompt_pos: The positive prompt to use to describe the textures

          prompt_neg: The negative prompt to use to describe the textures. default is 'deformed, ugly,
              blurred'

          seed: The seed to use for the generation (default is 1)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/components/texture_object",
            body=maybe_transform(
                {
                    "mesh_request_id": mesh_request_id,
                    "prompt_pos": prompt_pos,
                    "prompt_neg": prompt_neg,
                    "seed": seed,
                },
                component_texture_object_params.ComponentTextureObjectParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenerateResponseObject,
        )


class AsyncComponentsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncComponentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/masterpiecevr/mpx-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncComponentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncComponentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/masterpiecevr/mpx-sdk-python#with_streaming_response
        """
        return AsyncComponentsResourceWithStreamingResponse(self)

    async def animate(
        self,
        *,
        moves_like_prompt: str,
        seed: float | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GenerateResponseObject:
        """
        This function creates a BVH animation file suitable for standard rigged
        humanoids. Use the status endpoint to check the status of the request. Save the
        returned requestId for use with other components as input.

        Args:
          moves_like_prompt: The prompt to use to describe the animation

          seed: The seed to use for the generation (default is 1)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/components/animate",
            body=await async_maybe_transform(
                {
                    "moves_like_prompt": moves_like_prompt,
                    "seed": seed,
                },
                component_animate_params.ComponentAnimateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenerateResponseObject,
        )

    async def base_mesh_gen(
        self,
        *,
        category: str,
        mesh_type: str,
        mesh_variability: float,
        text_prompt: str,
        image_request_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GenerateResponseObject:
        """
        This function uses a generative approach to create an OBJ model that you can use
        for further processing. It takes an image and/or a text as input and may create
        a more unique and creative model than the base mesh selector. You can supply an
        image and/or a text prompt as input. This component does not generate a UV map
        or textures. You can use the generated OBJ file as the base mesh for creating a
        thumbnail or as an input for texturing or animation. Use the status endpoint to
        check the status of the request. Save the returned requestId for use with other
        components as input.

        Args:
          category: The category of the mesh to use for the generation. One or two words that
              describe the mesh. eg. 'sports ball', 'chair', 'table'

          mesh_type: The type of mesh to use for the generation. Allowed values are (object, animal,
              humanoid)

          mesh_variability: The variability of the mesh to use for the generation

          text_prompt: The prompt to use for the generation of the mesh. can be an empty string if
              imageRequestId is provided.

          image_request_id: The requestId from the /assets/create endpoint that the image was uploaded to

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/components/base_mesh_gen",
            body=await async_maybe_transform(
                {
                    "category": category,
                    "mesh_type": mesh_type,
                    "mesh_variability": mesh_variability,
                    "text_prompt": text_prompt,
                    "image_request_id": image_request_id,
                },
                component_base_mesh_gen_params.ComponentBaseMeshGenParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenerateResponseObject,
        )

    async def base_mesh_select(
        self,
        *,
        category: str,
        mesh_type: str,
        mesh_variability: float,
        text_prompt: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GenerateResponseObject:
        """This function selects a model from a curated library using RAG.

        Use this
        function to select a conservative but high quality model for your project. This
        component does not generate a UV map or textures. It returns an OBJ file that
        you can use for further processing. You can use this OBJ file as the base mesh
        for creating a thumbnail or as an input for texturing or animation. Use the
        status endpoint to check the status of the request. Save the returned requestId
        for use with other components as input.

        Args:
          category: The category of the mesh to use for the generation. Allowed values are (object,
              animal, humanoid)

          mesh_type: The type of mesh to use for the generation. Allowed values are (object, animal,
              humanoid)

          mesh_variability: The variability of the mesh to use for the generation

          text_prompt: The prompt to use for the generation of the mesh

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/components/base_mesh_select",
            body=await async_maybe_transform(
                {
                    "category": category,
                    "mesh_type": mesh_type,
                    "mesh_variability": mesh_variability,
                    "text_prompt": text_prompt,
                },
                component_base_mesh_select_params.ComponentBaseMeshSelectParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenerateResponseObject,
        )

    async def generate_glb(
        self,
        *,
        mesh_request_id: str,
        mesh_type: str,
        texture_request_id: str,
        animation_request_id: str | NotGiven = NOT_GIVEN,
        rig_only: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GenerateResponseObject:
        """
        This function takes a UV'd OBJ model, a texture and optionally an animation and
        creates a GLB file that you can use for further processing. It also creates a
        thumbnail image, an FBX and USDZ file. Use the requestId from the
        **texture_object** endpoint for both the model and texture as input unless you
        are using an asset that has been uploaded. Use the requestId from the
        **animation** endpoint for the animation. Use the status endpoint to check the
        status of the request. Save the returned requestId for use with other components
        as input. Note that the outputUrl will be the URL of the GLB file. Other file
        types are available in the outputs object. Note that the **rigOnly** flag is
        optional and defaults to false. It only applies if the **meshType** is human. If
        set to true and the model is human, the model will be returned rigged and
        skinned in T-pose with no animation.

        Args:
          mesh_request_id: The requestId from the /assets/create endpoint that the model was uploaded to

          mesh_type: The type of mesh to use for the generation. Allowed values are (object, animal,
              humanoid)

          texture_request_id: The requestId from the /assets/create endpoint that the texture was uploaded to

          animation_request_id: The requestId from the /components/animate endpoint that the animation was
              uploaded to

          rig_only: Whether to return only a rigged and skinned model in T-pose with no animation.
              defaults to false. Note that not providing an animationRequestId and setting
              this to true will return a rigged and skinned model in T-pose with no animation.
              Not providing an animationRequestId and setting this to false will return a
              UV-ed model with no rigging or skinning. Providing an animationRequestId will
              override this setting and return a rigged and animated model.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/components/generate_glb",
            body=await async_maybe_transform(
                {
                    "mesh_request_id": mesh_request_id,
                    "mesh_type": mesh_type,
                    "texture_request_id": texture_request_id,
                    "animation_request_id": animation_request_id,
                    "rig_only": rig_only,
                },
                component_generate_glb_params.ComponentGenerateGlbParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenerateResponseObject,
        )

    async def optimize(
        self,
        *,
        asset_request_id: str,
        object_type: str,
        output_file_format: str,
        target_ratio: float,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CreateResponseObject:
        """
        This function optionally reduces the polycount of your model and/or returns a
        different file format. eg. convert from GLB to USDZ.

        The **assetRequestId** can be a requestId from a **Generate** request or an
        assetId from an **assets/create** request. If you are converting a model you
        uploaded, please ensure that the model has been uploaded before calling this
        endpoint.

        The **targetRatio** is the ratio of the original polycount that you want to
        reduce to. eg. 0.5 will reduce the polycount by 50%.

        The **outputFileFormat** is the file format you want the model returned in.
        Currently, we support FBX, GLB and USDZ.

        The **objectType** is the type of model you are uploading. Currently, we support
        'object', 'animal' and 'humanoid'.

        Args:
          asset_request_id: The requestId from the /assets/create endpoint that the model was uploaded to

          object_type: The type of model you are uploading. Currently, we support 'object', 'animal'
              and 'humanoid'.

          output_file_format: The file format you want the model returned in. Currently, we support FBX, GLB
              and USDZ.

          target_ratio: The ratio of the original polycount that you want to reduce to. eg. 0.5 will
              reduce the polycount by 50%.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/components/optimize",
            body=await async_maybe_transform(
                {
                    "asset_request_id": asset_request_id,
                    "object_type": object_type,
                    "output_file_format": output_file_format,
                    "target_ratio": target_ratio,
                },
                component_optimize_params.ComponentOptimizeParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CreateResponseObject,
        )

    async def texture_animals_humanoids(
        self,
        *,
        mesh_request_id: str,
        prompt_pos: str,
        prompt_neg: str | NotGiven = NOT_GIVEN,
        seed: float | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GenerateResponseObject:
        """
        This function creates a UV mapped version of the input OBJ model and generates a
        texture mapped png file. Use the requestId from the **base_mesh_select** or
        **mesh_gen** endpoint or an asset that has been uploaded as input. Use the seed
        to generate a different texture for the same model. Use this function to create
        a textured model from a base mesh or a generated mesh. It is primarily used for
        animals and humanoids. Use the status endpoint to check the status of the
        request. Save the returned requestId for use with other components as input.

        Args:
          mesh_request_id: The requestId from the /assets/create endpoint that the model was uploaded to

          prompt_pos: The positive prompt to use to describe the textures

          prompt_neg: The negative prompt to use to describe the textures. default is 'deformed, ugly,
              blurred'

          seed: The seed to use for the generation (default is 1)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/components/texture",
            body=await async_maybe_transform(
                {
                    "mesh_request_id": mesh_request_id,
                    "prompt_pos": prompt_pos,
                    "prompt_neg": prompt_neg,
                    "seed": seed,
                },
                component_texture_animals_humanoids_params.ComponentTextureAnimalsHumanoidsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenerateResponseObject,
        )

    async def texture_object(
        self,
        *,
        mesh_request_id: str,
        prompt_pos: str,
        prompt_neg: str | NotGiven = NOT_GIVEN,
        seed: float | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GenerateResponseObject:
        """
        This function creates a UV mapped version of the input OBJ model and generates a
        texture mapped png file. Use the requestId from the **base_mesh_select** or
        **mesh_gen** endpoint or an asset that has been uploaded as input. Use the seed
        to generate a different texture for the same model. Use this function to create
        a textured model from a base mesh or a generated mesh. It is primarily used for
        objects, not humanoids. Use the status endpoint to check the status of the
        request. Save the returned requestId for use with other components as input.

        Args:
          mesh_request_id: The requestId from the /assets/create endpoint that the model was uploaded to

          prompt_pos: The positive prompt to use to describe the textures

          prompt_neg: The negative prompt to use to describe the textures. default is 'deformed, ugly,
              blurred'

          seed: The seed to use for the generation (default is 1)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/components/texture_object",
            body=await async_maybe_transform(
                {
                    "mesh_request_id": mesh_request_id,
                    "prompt_pos": prompt_pos,
                    "prompt_neg": prompt_neg,
                    "seed": seed,
                },
                component_texture_object_params.ComponentTextureObjectParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenerateResponseObject,
        )


class ComponentsResourceWithRawResponse:
    def __init__(self, components: ComponentsResource) -> None:
        self._components = components

        self.animate = to_raw_response_wrapper(
            components.animate,
        )
        self.base_mesh_gen = to_raw_response_wrapper(
            components.base_mesh_gen,
        )
        self.base_mesh_select = to_raw_response_wrapper(
            components.base_mesh_select,
        )
        self.generate_glb = to_raw_response_wrapper(
            components.generate_glb,
        )
        self.optimize = to_raw_response_wrapper(
            components.optimize,
        )
        self.texture_animals_humanoids = to_raw_response_wrapper(
            components.texture_animals_humanoids,
        )
        self.texture_object = to_raw_response_wrapper(
            components.texture_object,
        )


class AsyncComponentsResourceWithRawResponse:
    def __init__(self, components: AsyncComponentsResource) -> None:
        self._components = components

        self.animate = async_to_raw_response_wrapper(
            components.animate,
        )
        self.base_mesh_gen = async_to_raw_response_wrapper(
            components.base_mesh_gen,
        )
        self.base_mesh_select = async_to_raw_response_wrapper(
            components.base_mesh_select,
        )
        self.generate_glb = async_to_raw_response_wrapper(
            components.generate_glb,
        )
        self.optimize = async_to_raw_response_wrapper(
            components.optimize,
        )
        self.texture_animals_humanoids = async_to_raw_response_wrapper(
            components.texture_animals_humanoids,
        )
        self.texture_object = async_to_raw_response_wrapper(
            components.texture_object,
        )


class ComponentsResourceWithStreamingResponse:
    def __init__(self, components: ComponentsResource) -> None:
        self._components = components

        self.animate = to_streamed_response_wrapper(
            components.animate,
        )
        self.base_mesh_gen = to_streamed_response_wrapper(
            components.base_mesh_gen,
        )
        self.base_mesh_select = to_streamed_response_wrapper(
            components.base_mesh_select,
        )
        self.generate_glb = to_streamed_response_wrapper(
            components.generate_glb,
        )
        self.optimize = to_streamed_response_wrapper(
            components.optimize,
        )
        self.texture_animals_humanoids = to_streamed_response_wrapper(
            components.texture_animals_humanoids,
        )
        self.texture_object = to_streamed_response_wrapper(
            components.texture_object,
        )


class AsyncComponentsResourceWithStreamingResponse:
    def __init__(self, components: AsyncComponentsResource) -> None:
        self._components = components

        self.animate = async_to_streamed_response_wrapper(
            components.animate,
        )
        self.base_mesh_gen = async_to_streamed_response_wrapper(
            components.base_mesh_gen,
        )
        self.base_mesh_select = async_to_streamed_response_wrapper(
            components.base_mesh_select,
        )
        self.generate_glb = async_to_streamed_response_wrapper(
            components.generate_glb,
        )
        self.optimize = async_to_streamed_response_wrapper(
            components.optimize,
        )
        self.texture_animals_humanoids = async_to_streamed_response_wrapper(
            components.texture_animals_humanoids,
        )
        self.texture_object = async_to_streamed_response_wrapper(
            components.texture_object,
        )
