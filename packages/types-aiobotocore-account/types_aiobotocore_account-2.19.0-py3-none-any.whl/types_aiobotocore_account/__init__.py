"""
Main interface for account service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_account import (
        AccountClient,
        Client,
        ListRegionsPaginator,
    )

    session = get_session()
    async with session.create_client("account") as client:
        client: AccountClient
        ...


    list_regions_paginator: ListRegionsPaginator = client.get_paginator("list_regions")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import AccountClient
from .paginator import ListRegionsPaginator

Client = AccountClient


__all__ = ("AccountClient", "Client", "ListRegionsPaginator")
