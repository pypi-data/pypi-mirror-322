"""
Main interface for mediastore-data service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_mediastore_data import (
        Client,
        ListItemsPaginator,
        MediaStoreDataClient,
    )

    session = get_session()
    async with session.create_client("mediastore-data") as client:
        client: MediaStoreDataClient
        ...


    list_items_paginator: ListItemsPaginator = client.get_paginator("list_items")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import MediaStoreDataClient
from .paginator import ListItemsPaginator

Client = MediaStoreDataClient

__all__ = ("Client", "ListItemsPaginator", "MediaStoreDataClient")
