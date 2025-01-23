from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.collection import Collection
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    name: str,
    *,
    is_exact: Union[Unset, bool] = False,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["is_exact"] = is_exact

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/collection/get/{name}",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Collection, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = Collection.from_dict(response.json())

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
) -> Response[Union[Any, Collection, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    name: str,
    *,
    client: AuthenticatedClient,
    is_exact: Union[Unset, bool] = False,
) -> Response[Union[Any, Collection, HTTPValidationError]]:
    """Get Collection

     Get a collection

    Args:
        name (str):
        is_exact (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Collection, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        name=name,
        is_exact=is_exact,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    name: str,
    *,
    client: AuthenticatedClient,
    is_exact: Union[Unset, bool] = False,
) -> Optional[Union[Any, Collection, HTTPValidationError]]:
    """Get Collection

     Get a collection

    Args:
        name (str):
        is_exact (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Collection, HTTPValidationError]
    """

    return sync_detailed(
        name=name,
        client=client,
        is_exact=is_exact,
    ).parsed


async def asyncio_detailed(
    name: str,
    *,
    client: AuthenticatedClient,
    is_exact: Union[Unset, bool] = False,
) -> Response[Union[Any, Collection, HTTPValidationError]]:
    """Get Collection

     Get a collection

    Args:
        name (str):
        is_exact (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Collection, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        name=name,
        is_exact=is_exact,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    name: str,
    *,
    client: AuthenticatedClient,
    is_exact: Union[Unset, bool] = False,
) -> Optional[Union[Any, Collection, HTTPValidationError]]:
    """Get Collection

     Get a collection

    Args:
        name (str):
        is_exact (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Collection, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
            is_exact=is_exact,
        )
    ).parsed
