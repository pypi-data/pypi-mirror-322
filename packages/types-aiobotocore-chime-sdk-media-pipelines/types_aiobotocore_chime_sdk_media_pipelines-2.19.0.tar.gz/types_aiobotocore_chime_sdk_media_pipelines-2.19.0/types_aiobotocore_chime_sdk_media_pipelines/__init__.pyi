"""
Main interface for chime-sdk-media-pipelines service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_chime_sdk_media_pipelines import (
        ChimeSDKMediaPipelinesClient,
        Client,
    )

    session = get_session()
    async with session.create_client("chime-sdk-media-pipelines") as client:
        client: ChimeSDKMediaPipelinesClient
        ...

    ```

Copyright 2025 Vlad Emelianov
"""

from .client import ChimeSDKMediaPipelinesClient

Client = ChimeSDKMediaPipelinesClient

__all__ = ("ChimeSDKMediaPipelinesClient", "Client")
