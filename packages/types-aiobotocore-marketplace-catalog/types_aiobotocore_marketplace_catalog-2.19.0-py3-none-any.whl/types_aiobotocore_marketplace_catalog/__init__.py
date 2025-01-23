"""
Main interface for marketplace-catalog service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_marketplace_catalog import (
        Client,
        ListChangeSetsPaginator,
        ListEntitiesPaginator,
        MarketplaceCatalogClient,
    )

    session = get_session()
    async with session.create_client("marketplace-catalog") as client:
        client: MarketplaceCatalogClient
        ...


    list_change_sets_paginator: ListChangeSetsPaginator = client.get_paginator("list_change_sets")
    list_entities_paginator: ListEntitiesPaginator = client.get_paginator("list_entities")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import MarketplaceCatalogClient
from .paginator import ListChangeSetsPaginator, ListEntitiesPaginator

Client = MarketplaceCatalogClient


__all__ = ("Client", "ListChangeSetsPaginator", "ListEntitiesPaginator", "MarketplaceCatalogClient")
