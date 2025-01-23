"""
Main interface for sqs service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_sqs import (
        Client,
        ListDeadLetterSourceQueuesPaginator,
        ListQueuesPaginator,
        SQSClient,
        SQSServiceResource,
        ServiceResource,
    )

    session = get_session()
    async with session.create_client("sqs") as client:
        client: SQSClient
        ...


    list_dead_letter_source_queues_paginator: ListDeadLetterSourceQueuesPaginator = client.get_paginator("list_dead_letter_source_queues")
    list_queues_paginator: ListQueuesPaginator = client.get_paginator("list_queues")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import SQSClient
from .paginator import ListDeadLetterSourceQueuesPaginator, ListQueuesPaginator

try:
    from .service_resource import SQSServiceResource
except ImportError:
    from builtins import object as SQSServiceResource  # type: ignore[assignment]

Client = SQSClient

ServiceResource = SQSServiceResource

__all__ = (
    "Client",
    "ListDeadLetterSourceQueuesPaginator",
    "ListQueuesPaginator",
    "SQSClient",
    "SQSServiceResource",
    "ServiceResource",
)
