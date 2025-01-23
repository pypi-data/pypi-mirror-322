from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    name: str,
    limit: Union[None, Unset, int] = UNSET,
    total_only: Union[None, Unset, bool] = False,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["name"] = name

    json_limit: Union[None, Unset, int]
    if isinstance(limit, Unset):
        json_limit = UNSET
    else:
        json_limit = limit
    params["limit"] = json_limit

    json_total_only: Union[None, Unset, bool]
    if isinstance(total_only, Unset):
        json_total_only = UNSET
    else:
        json_total_only = total_only
    params["total_only"] = json_total_only

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/exact/counter/dupes",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError, Union[int, list[list[Any]]]]]:
    if response.status_code == 200:

        def _parse_response_200(data: object) -> Union[int, list[list[Any]]]:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                response_200_type_0 = []
                _response_200_type_0 = data
                for response_200_type_0_item_data in _response_200_type_0:
                    response_200_type_0_item = cast(list[Any], response_200_type_0_item_data)

                    response_200_type_0.append(response_200_type_0_item)

                return response_200_type_0
            except:  # noqa: E722
                pass
            return cast(Union[int, list[list[Any]]], data)

        response_200 = _parse_response_200(response.json())

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
) -> Response[Union[Any, HTTPValidationError, Union[int, list[list[Any]]]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    name: str,
    limit: Union[None, Unset, int] = UNSET,
    total_only: Union[None, Unset, bool] = False,
) -> Response[Union[Any, HTTPValidationError, Union[int, list[list[Any]]]]]:
    """Dupes List

    Args:
        name (str):
        limit (Union[None, Unset, int]):
        total_only (Union[None, Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, Union[int, list[list[Any]]]]]
    """

    kwargs = _get_kwargs(
        name=name,
        limit=limit,
        total_only=total_only,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    name: str,
    limit: Union[None, Unset, int] = UNSET,
    total_only: Union[None, Unset, bool] = False,
) -> Optional[Union[Any, HTTPValidationError, Union[int, list[list[Any]]]]]:
    """Dupes List

    Args:
        name (str):
        limit (Union[None, Unset, int]):
        total_only (Union[None, Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, Union[int, list[list[Any]]]]
    """

    return sync_detailed(
        client=client,
        name=name,
        limit=limit,
        total_only=total_only,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    name: str,
    limit: Union[None, Unset, int] = UNSET,
    total_only: Union[None, Unset, bool] = False,
) -> Response[Union[Any, HTTPValidationError, Union[int, list[list[Any]]]]]:
    """Dupes List

    Args:
        name (str):
        limit (Union[None, Unset, int]):
        total_only (Union[None, Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, Union[int, list[list[Any]]]]]
    """

    kwargs = _get_kwargs(
        name=name,
        limit=limit,
        total_only=total_only,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    name: str,
    limit: Union[None, Unset, int] = UNSET,
    total_only: Union[None, Unset, bool] = False,
) -> Optional[Union[Any, HTTPValidationError, Union[int, list[list[Any]]]]]:
    """Dupes List

    Args:
        name (str):
        limit (Union[None, Unset, int]):
        total_only (Union[None, Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, Union[int, list[list[Any]]]]
    """

    return (
        await asyncio_detailed(
            client=client,
            name=name,
            limit=limit,
            total_only=total_only,
        )
    ).parsed
