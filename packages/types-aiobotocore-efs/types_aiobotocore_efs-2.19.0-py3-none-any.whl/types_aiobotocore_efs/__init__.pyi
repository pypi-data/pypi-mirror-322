"""
Main interface for efs service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_efs import (
        Client,
        DescribeAccessPointsPaginator,
        DescribeFileSystemsPaginator,
        DescribeMountTargetsPaginator,
        DescribeReplicationConfigurationsPaginator,
        DescribeTagsPaginator,
        EFSClient,
    )

    session = get_session()
    async with session.create_client("efs") as client:
        client: EFSClient
        ...


    describe_access_points_paginator: DescribeAccessPointsPaginator = client.get_paginator("describe_access_points")
    describe_file_systems_paginator: DescribeFileSystemsPaginator = client.get_paginator("describe_file_systems")
    describe_mount_targets_paginator: DescribeMountTargetsPaginator = client.get_paginator("describe_mount_targets")
    describe_replication_configurations_paginator: DescribeReplicationConfigurationsPaginator = client.get_paginator("describe_replication_configurations")
    describe_tags_paginator: DescribeTagsPaginator = client.get_paginator("describe_tags")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import EFSClient
from .paginator import (
    DescribeAccessPointsPaginator,
    DescribeFileSystemsPaginator,
    DescribeMountTargetsPaginator,
    DescribeReplicationConfigurationsPaginator,
    DescribeTagsPaginator,
)

Client = EFSClient

__all__ = (
    "Client",
    "DescribeAccessPointsPaginator",
    "DescribeFileSystemsPaginator",
    "DescribeMountTargetsPaginator",
    "DescribeReplicationConfigurationsPaginator",
    "DescribeTagsPaginator",
    "EFSClient",
)
