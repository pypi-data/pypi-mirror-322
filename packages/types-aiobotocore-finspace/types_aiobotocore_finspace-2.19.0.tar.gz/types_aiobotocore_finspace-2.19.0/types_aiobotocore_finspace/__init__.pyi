"""
Main interface for finspace service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_finspace import (
        Client,
        FinspaceClient,
        ListKxEnvironmentsPaginator,
    )

    session = get_session()
    async with session.create_client("finspace") as client:
        client: FinspaceClient
        ...


    list_kx_environments_paginator: ListKxEnvironmentsPaginator = client.get_paginator("list_kx_environments")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import FinspaceClient
from .paginator import ListKxEnvironmentsPaginator

Client = FinspaceClient

__all__ = ("Client", "FinspaceClient", "ListKxEnvironmentsPaginator")
