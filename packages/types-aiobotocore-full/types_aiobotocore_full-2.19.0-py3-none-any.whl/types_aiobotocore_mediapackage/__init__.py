"""
Main interface for mediapackage service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_mediapackage import (
        Client,
        ListChannelsPaginator,
        ListHarvestJobsPaginator,
        ListOriginEndpointsPaginator,
        MediaPackageClient,
    )

    session = get_session()
    async with session.create_client("mediapackage") as client:
        client: MediaPackageClient
        ...


    list_channels_paginator: ListChannelsPaginator = client.get_paginator("list_channels")
    list_harvest_jobs_paginator: ListHarvestJobsPaginator = client.get_paginator("list_harvest_jobs")
    list_origin_endpoints_paginator: ListOriginEndpointsPaginator = client.get_paginator("list_origin_endpoints")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import MediaPackageClient
from .paginator import ListChannelsPaginator, ListHarvestJobsPaginator, ListOriginEndpointsPaginator

Client = MediaPackageClient


__all__ = (
    "Client",
    "ListChannelsPaginator",
    "ListHarvestJobsPaginator",
    "ListOriginEndpointsPaginator",
    "MediaPackageClient",
)
