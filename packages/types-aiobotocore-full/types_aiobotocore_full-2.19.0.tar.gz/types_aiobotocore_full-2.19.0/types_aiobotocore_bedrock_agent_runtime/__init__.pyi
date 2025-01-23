"""
Main interface for bedrock-agent-runtime service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_bedrock_agent_runtime import (
        AgentsforBedrockRuntimeClient,
        Client,
        GetAgentMemoryPaginator,
        RerankPaginator,
        RetrievePaginator,
    )

    session = get_session()
    async with session.create_client("bedrock-agent-runtime") as client:
        client: AgentsforBedrockRuntimeClient
        ...


    get_agent_memory_paginator: GetAgentMemoryPaginator = client.get_paginator("get_agent_memory")
    rerank_paginator: RerankPaginator = client.get_paginator("rerank")
    retrieve_paginator: RetrievePaginator = client.get_paginator("retrieve")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import AgentsforBedrockRuntimeClient
from .paginator import GetAgentMemoryPaginator, RerankPaginator, RetrievePaginator

Client = AgentsforBedrockRuntimeClient

__all__ = (
    "AgentsforBedrockRuntimeClient",
    "Client",
    "GetAgentMemoryPaginator",
    "RerankPaginator",
    "RetrievePaginator",
)
