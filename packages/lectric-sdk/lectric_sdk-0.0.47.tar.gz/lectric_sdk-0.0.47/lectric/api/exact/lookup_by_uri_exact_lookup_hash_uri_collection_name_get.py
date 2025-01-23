from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    collection_name: str,
    *,
    uri: str,
    fk: Union[None, Unset, str] = UNSET,
    caller: Union[None, Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["uri"] = uri

    json_fk: Union[None, Unset, str]
    if isinstance(fk, Unset):
        json_fk = UNSET
    else:
        json_fk = fk
    params["fk"] = json_fk

    json_caller: Union[None, Unset, str]
    if isinstance(caller, Unset):
        json_caller = UNSET
    else:
        json_caller = caller
    params["caller"] = json_caller

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/exact/lookup/hash/uri/{collection_name}",
        "params": params,
    }

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
    uri: str,
    fk: Union[None, Unset, str] = UNSET,
    caller: Union[None, Unset, str] = UNSET,
) -> Response[Union[Any, HTTPValidationError]]:
    """Lookup By Uri

     Lookup in a collection using a URI

    Args:
        collection_name (str):
        uri (str):
        fk (Union[None, Unset, str]):
        caller (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        collection_name=collection_name,
        uri=uri,
        fk=fk,
        caller=caller,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    collection_name: str,
    *,
    client: AuthenticatedClient,
    uri: str,
    fk: Union[None, Unset, str] = UNSET,
    caller: Union[None, Unset, str] = UNSET,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Lookup By Uri

     Lookup in a collection using a URI

    Args:
        collection_name (str):
        uri (str):
        fk (Union[None, Unset, str]):
        caller (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return sync_detailed(
        collection_name=collection_name,
        client=client,
        uri=uri,
        fk=fk,
        caller=caller,
    ).parsed


async def asyncio_detailed(
    collection_name: str,
    *,
    client: AuthenticatedClient,
    uri: str,
    fk: Union[None, Unset, str] = UNSET,
    caller: Union[None, Unset, str] = UNSET,
) -> Response[Union[Any, HTTPValidationError]]:
    """Lookup By Uri

     Lookup in a collection using a URI

    Args:
        collection_name (str):
        uri (str):
        fk (Union[None, Unset, str]):
        caller (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        collection_name=collection_name,
        uri=uri,
        fk=fk,
        caller=caller,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    collection_name: str,
    *,
    client: AuthenticatedClient,
    uri: str,
    fk: Union[None, Unset, str] = UNSET,
    caller: Union[None, Unset, str] = UNSET,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Lookup By Uri

     Lookup in a collection using a URI

    Args:
        collection_name (str):
        uri (str):
        fk (Union[None, Unset, str]):
        caller (Union[None, Unset, str]):

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
            uri=uri,
            fk=fk,
            caller=caller,
        )
    ).parsed
