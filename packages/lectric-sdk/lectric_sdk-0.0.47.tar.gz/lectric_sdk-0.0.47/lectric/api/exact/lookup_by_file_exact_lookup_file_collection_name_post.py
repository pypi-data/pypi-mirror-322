from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.body_lookup_by_file_exact_lookup_file_collection_name_post import (
    BodyLookupByFileExactLookupFileCollectionNamePost,
)
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    collection_name: str,
    *,
    body: BodyLookupByFileExactLookupFileCollectionNamePost,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/exact/lookup/file/{collection_name}",
    }

    _body = body.to_multipart()

    _kwargs["files"] = _body

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = response.json()
        return response_200
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    collection_name: str,
    *,
    client: AuthenticatedClient,
    body: BodyLookupByFileExactLookupFileCollectionNamePost,
) -> Response[Union[Any, HTTPValidationError]]:
    """Lookup By File

     Lookup into a collection using a file

    Args:
        collection_name (str):
        body (BodyLookupByFileExactLookupFileCollectionNamePost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        collection_name=collection_name,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    collection_name: str,
    *,
    client: AuthenticatedClient,
    body: BodyLookupByFileExactLookupFileCollectionNamePost,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Lookup By File

     Lookup into a collection using a file

    Args:
        collection_name (str):
        body (BodyLookupByFileExactLookupFileCollectionNamePost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return sync_detailed(
        collection_name=collection_name,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    collection_name: str,
    *,
    client: AuthenticatedClient,
    body: BodyLookupByFileExactLookupFileCollectionNamePost,
) -> Response[Union[Any, HTTPValidationError]]:
    """Lookup By File

     Lookup into a collection using a file

    Args:
        collection_name (str):
        body (BodyLookupByFileExactLookupFileCollectionNamePost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        collection_name=collection_name,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    collection_name: str,
    *,
    client: AuthenticatedClient,
    body: BodyLookupByFileExactLookupFileCollectionNamePost,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Lookup By File

     Lookup into a collection using a file

    Args:
        collection_name (str):
        body (BodyLookupByFileExactLookupFileCollectionNamePost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            collection_name=collection_name,
            client=client,
            body=body,
        )
    ).parsed
