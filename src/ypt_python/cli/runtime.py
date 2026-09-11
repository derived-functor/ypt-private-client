"""Shared runtime helpers for CLI commands."""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from typing import Any, TypeVar

import typer

from ypt_python import YPTClient
from ypt_python._exceptions import AuthenticationError
from ypt_python.cli.config import load_config, write_template
from ypt_python.cli.output import console

T = TypeVar("T")


async def _get_client() -> YPTClient:
    client = YPTClient(cache_token=True)
    if client.token is not None:
        return client
    write_template()
    cfg = load_config()
    if cfg.email and cfg.password:
        await client.auth.login(cfg.email, cfg.password)
        return client
    console.print("[red]Not logged in.[/] Run [bold]ypt-python login[/] first.", style="red")
    raise typer.Exit(1)


async def _authenticated(
    coro: Callable[..., Awaitable[T]],
    *args: Any,
    **kwargs: Any,
) -> T:
    client = await _get_client()
    try:
        return await coro(client, *args, **kwargs)
    except AuthenticationError:
        cfg = load_config()
        if not (cfg.email and cfg.password):
            raise
        await client.auth.login(cfg.email, cfg.password)
        return await coro(client, *args, **kwargs)


def authenticated(coro: Callable[..., Awaitable[T]]) -> Callable[..., T]:
    """Wrap an async command so it gets an authenticated client.

    Retries once with a fresh login when the cached token is stale.
    """

    def wrapper(*args: Any, **kwargs: Any) -> T:
        return asyncio.run(_authenticated(coro, *args, **kwargs))

    return wrapper


def make_client() -> YPTClient:
    return YPTClient(cache_token=True)


def run(coro: Callable[[], Awaitable[Any]]) -> Any:
    return asyncio.run(coro())