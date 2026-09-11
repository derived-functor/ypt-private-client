from __future__ import annotations

from typing import Any

import httpx

from ypt_python._exceptions import APIError, AuthenticationError, ServerError

_BASE_URL = "https://pi.tgclab.com"
_USER_AGENT = "Dart/3.11 (dart:io)"
_AUTH_ERROR_CODES = {"112", "113", "missing_jwt"}


class HTTPClient:
    def __init__(self, token: str | None = None) -> None:
        self._token = token
        self._client = httpx.AsyncClient(
            base_url=_BASE_URL,
            headers={
                "User-Agent": _USER_AGENT,
                "Content-Type": "application/json",
                "Accept-Encoding": "gzip",
            },
            timeout=30.0,
        )

    @property
    def token(self) -> str | None:
        return self._token

    @token.setter
    def token(self, value: str) -> None:
        self._token = value

    def _headers(self) -> dict[str, str]:
        headers: dict[str, str] = {}
        if self._token:
            headers["authorization"] = f"JWT {self._token}"
        return headers

    def _check(self, data: dict[str, Any]) -> dict[str, Any]:
        if data.get("s") is True:
            return data
        code = str(data.get("c", ""))
        if code in _AUTH_ERROR_CODES:
            raise AuthenticationError(code)
        if code == "alert_server_error_msg":
            raise ServerError()
        raise APIError(code)

    async def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        resp = await self._client.get(path, params=params, headers=self._headers())
        resp.raise_for_status()
        return self._check(resp.json())

    async def post(self, path: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        resp = await self._client.post(path, json=json, headers=self._headers())
        resp.raise_for_status()
        return self._check(resp.json())

    async def close(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> HTTPClient:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()
