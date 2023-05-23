import logging
from typing import Any, Dict, List, Optional

from httpx import AsyncClient, HTTPStatusError, Response

from aiokeepin.exceptions.base import (
    InternalServerError,
    InvalidAPIKeyError,
    KeepinStatusError,
    NotFoundError,
    ValidationError,
)

BASE_URL = "https://api.keepincrm.com/v1"
logger = logging.getLogger(__name__)


class BaseAdapter:
    def __init__(
        self,
        api_key: str,
        session: Optional[AsyncClient] = None,
        base_url: str = BASE_URL,
    ) -> None:
        """
        Base adapter for Keepin API.

        ### Args:
        - `api_key` (str): Keepin API key.
        - `session` (Optional[AsyncClient], optional): Async Client.
            Defaults to `None`.
        - `base_url` (str, optional): Base URL for the API. Defaults
            to `BASE_URL`.
        """
        self.api_key = api_key
        self.base_url = base_url
        self.session = session or AsyncClient()

    async def _request(
        self,
        path: str,
        *,
        method: str,
        params: Optional[Dict[str, Any]] = None,
        json: Any = None,
        data: Any = None,
    ) -> Response:
        if not path.startswith("https://"):
            path = self.base_url + path

        headers = {"X-Auth-Token": self.api_key}

        response = await self.session.request(
            method,
            path,
            params=params,
            data=data,
            json=json,
            headers=headers,
        )

        try:
            response.raise_for_status()
        except HTTPStatusError as e:
            status_code = e.response.status_code
            response_data = e.response.text
            if status_code == 401:
                raise InvalidAPIKeyError(status_code, response_data) from e
            if status_code == 422:
                raise ValidationError(status_code, response_data) from e
            if status_code == 404:
                raise NotFoundError(status_code, response_data) from e
            if status_code >= 500:
                raise InternalServerError(status_code, response_data) from e
            raise KeepinStatusError(status_code, response_data) from e

        return response

    async def post(
        self, path: str, json: Any, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make a POST request to the API.

        ### Args:
        - `path` (str): Path to the endpoint.
        - `json` (Any): JSON data to send.
        - `params` (Optional[Dict[str, Any]], optional): Query
            parameters. Defaults to `None`.

        ### Returns:
        - `Dict[str, Any]`: JSON response.
        """
        response = await self._request(
            path, method="post", json=json, params=params
        )
        return response.json()

    async def get(
        self, path: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make a GET request to the API.

        ### Args:
        - `path` (str): Path to the endpoint.
        - `params` (Optional[Dict[str, Any]], optional): Query
            parameters. Defaults to `None`.

        ### Returns:
        - `Dict[str, Any]`: JSON response.
        """
        response = await self._request(path, method="get", params=params)
        return response.json()

    async def patch(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json: Any = None,
    ) -> Dict[str, Any]:
        """
        Make a PATCH request to the API.

        ### Args:
        - `path` (str): Path to the endpoint.
        - `json` (Any): JSON data to send.
        - `params` (Optional[Dict[str, Any]], optional): Query
            parameters. Defaults to `None`.

        ### Returns:
        - `Dict[str, Any]`: JSON response.
        """
        response = await self._request(
            path, method="patch", params=params, json=json
        )
        return response.json()

    async def delete(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json: Any = None,
    ) -> Dict[str, Any]:
        """
        Make a DELETE request to the API.

        ### Args:
        - `path` (str): Path to the endpoint.
        - `json` (Any): JSON data to send.
        - `params` (Optional[Dict[str, Any]], optional): Query
            parameters. Defaults to `None`.

        ### Returns:
        - `Dict[str, Any]`: JSON response.
        """
        response = await self._request(
            path, method="delete", params=params, json=json
        )
        return response.json()

    async def put(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json: Any = None,
    ) -> Dict[str, Any]:
        """
        Make a PUT request to the API.

        ### Args:
        - `path` (str): Path to the endpoint.
        - `json` (Any): JSON data to send.
        - `params` (Optional[Dict[str, Any]], optional): Query
            parameters. Defaults to `None`.

        ### Returns:
        - `Dict[str, Any]`: JSON response.
        """
        response = await self._request(
            path, method="put", params=params, json=json
        )
        return response.json()

    async def close(self) -> None:
        """Close the session."""
        await self.session.close()

    async def get_paginated_items(
        self,
        path: str,
        count: Optional[int] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> List[Dict]:
        """
        Get all items from a paginated endpoint.

        ### Args:
        - `path` (str): Path to the endpoint.
        - `count` (Optional[int], optional): Number of items to get.
            Defaults to `None`.
        - `params` (Optional[Dict[str, Any]], optional): Query
            parameters. Defaults to `None`.

        ### Returns:
        - `List[Dict]`: List of items.
        """

        items = []

        if not params:
            params = {}

        page = 1
        total_pages = 1

        if not count:
            condition = lambda: page <= total_pages
        else:
            condition = lambda: len(items) < count and page <= total_pages

        while True:
            params["page"] = page

            respone_data = await self.get(path, params=params)

            items += respone_data["items"]

            total_pages = respone_data["pagination"]["total_pages"]
            page += 1

            if not condition():
                break

        return items[:count]
