# Shared Types

```python
from mpx_genai_sdk.types import CreateResponseObject, GenerateResponseObject, GenFunctionPayload
```

# ConnectionTest

Types:

```python
from mpx_genai_sdk.types import ConnectionTestRetrieveResponse
```

Methods:

- <code title="get /connection/test">client.connection_test.<a href="./src/mpx_genai_sdk/resources/connection_test.py">retrieve</a>() -> str</code>

# Functions

Methods:

- <code title="post /functions/human">client.functions.<a href="./src/mpx_genai_sdk/resources/functions.py">animate_human</a>(\*\*<a href="src/mpx_genai_sdk/types/function_animate_human_params.py">params</a>) -> <a href="./src/mpx_genai_sdk/types/shared/generate_response_object.py">GenerateResponseObject</a></code>
- <code title="post /functions/animal">client.functions.<a href="./src/mpx_genai_sdk/resources/functions.py">create_animal</a>(\*\*<a href="src/mpx_genai_sdk/types/function_create_animal_params.py">params</a>) -> <a href="./src/mpx_genai_sdk/types/shared/generate_response_object.py">GenerateResponseObject</a></code>
- <code title="post /functions/general">client.functions.<a href="./src/mpx_genai_sdk/resources/functions.py">create_general</a>(\*\*<a href="src/mpx_genai_sdk/types/function_create_general_params.py">params</a>) -> <a href="./src/mpx_genai_sdk/types/shared/generate_response_object.py">GenerateResponseObject</a></code>
- <code title="post /functions/object">client.functions.<a href="./src/mpx_genai_sdk/resources/functions.py">create_object</a>(\*\*<a href="src/mpx_genai_sdk/types/function_create_object_params.py">params</a>) -> <a href="./src/mpx_genai_sdk/types/shared/generate_response_object.py">GenerateResponseObject</a></code>
- <code title="post /functions/imageto3d">client.functions.<a href="./src/mpx_genai_sdk/resources/functions.py">imageto3d</a>(\*\*<a href="src/mpx_genai_sdk/types/function_imageto3d_params.py">params</a>) -> <a href="./src/mpx_genai_sdk/types/shared/generate_response_object.py">GenerateResponseObject</a></code>

# Components

Methods:

- <code title="post /components/animate">client.components.<a href="./src/mpx_genai_sdk/resources/components.py">animate</a>(\*\*<a href="src/mpx_genai_sdk/types/component_animate_params.py">params</a>) -> <a href="./src/mpx_genai_sdk/types/shared/generate_response_object.py">GenerateResponseObject</a></code>
- <code title="post /components/base_mesh_gen">client.components.<a href="./src/mpx_genai_sdk/resources/components.py">base_mesh_gen</a>(\*\*<a href="src/mpx_genai_sdk/types/component_base_mesh_gen_params.py">params</a>) -> <a href="./src/mpx_genai_sdk/types/shared/generate_response_object.py">GenerateResponseObject</a></code>
- <code title="post /components/base_mesh_select">client.components.<a href="./src/mpx_genai_sdk/resources/components.py">base_mesh_select</a>(\*\*<a href="src/mpx_genai_sdk/types/component_base_mesh_select_params.py">params</a>) -> <a href="./src/mpx_genai_sdk/types/shared/generate_response_object.py">GenerateResponseObject</a></code>
- <code title="post /components/generate_glb">client.components.<a href="./src/mpx_genai_sdk/resources/components.py">generate_glb</a>(\*\*<a href="src/mpx_genai_sdk/types/component_generate_glb_params.py">params</a>) -> <a href="./src/mpx_genai_sdk/types/shared/generate_response_object.py">GenerateResponseObject</a></code>
- <code title="post /components/optimize">client.components.<a href="./src/mpx_genai_sdk/resources/components.py">optimize</a>(\*\*<a href="src/mpx_genai_sdk/types/component_optimize_params.py">params</a>) -> <a href="./src/mpx_genai_sdk/types/shared/create_response_object.py">CreateResponseObject</a></code>
- <code title="post /components/texture">client.components.<a href="./src/mpx_genai_sdk/resources/components.py">texture_animals_humanoids</a>(\*\*<a href="src/mpx_genai_sdk/types/component_texture_animals_humanoids_params.py">params</a>) -> <a href="./src/mpx_genai_sdk/types/shared/generate_response_object.py">GenerateResponseObject</a></code>
- <code title="post /components/texture_object">client.components.<a href="./src/mpx_genai_sdk/resources/components.py">texture_object</a>(\*\*<a href="src/mpx_genai_sdk/types/component_texture_object_params.py">params</a>) -> <a href="./src/mpx_genai_sdk/types/shared/generate_response_object.py">GenerateResponseObject</a></code>

# Assets

Methods:

- <code title="post /assets/create">client.assets.<a href="./src/mpx_genai_sdk/resources/assets.py">create</a>(\*\*<a href="src/mpx_genai_sdk/types/asset_create_params.py">params</a>) -> <a href="./src/mpx_genai_sdk/types/shared/create_response_object.py">CreateResponseObject</a></code>

# Status

Types:

```python
from mpx_genai_sdk.types import StatusResponseObject
```

Methods:

- <code title="get /status/{requestId}">client.status.<a href="./src/mpx_genai_sdk/resources/status.py">retrieve</a>(request_id) -> <a href="./src/mpx_genai_sdk/types/status_response_object.py">StatusResponseObject</a></code>
