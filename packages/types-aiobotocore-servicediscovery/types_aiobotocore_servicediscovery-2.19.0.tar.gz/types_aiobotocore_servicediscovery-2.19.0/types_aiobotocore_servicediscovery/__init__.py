"""
Main interface for servicediscovery service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_servicediscovery import (
        Client,
        ListInstancesPaginator,
        ListNamespacesPaginator,
        ListOperationsPaginator,
        ListServicesPaginator,
        ServiceDiscoveryClient,
    )

    session = get_session()
    async with session.create_client("servicediscovery") as client:
        client: ServiceDiscoveryClient
        ...


    list_instances_paginator: ListInstancesPaginator = client.get_paginator("list_instances")
    list_namespaces_paginator: ListNamespacesPaginator = client.get_paginator("list_namespaces")
    list_operations_paginator: ListOperationsPaginator = client.get_paginator("list_operations")
    list_services_paginator: ListServicesPaginator = client.get_paginator("list_services")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import ServiceDiscoveryClient
from .paginator import (
    ListInstancesPaginator,
    ListNamespacesPaginator,
    ListOperationsPaginator,
    ListServicesPaginator,
)

Client = ServiceDiscoveryClient


__all__ = (
    "Client",
    "ListInstancesPaginator",
    "ListNamespacesPaginator",
    "ListOperationsPaginator",
    "ListServicesPaginator",
    "ServiceDiscoveryClient",
)
