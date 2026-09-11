from __future__ import annotations

import getpass
from datetime import date

import typer
from rich.panel import Panel

from ypt_python._models import DayLog
from ypt_python.cli.config import load_config, write_credentials, write_template
from ypt_python.cli.output import console, format_ms, make_subject_table
from ypt_python.cli.runtime import YPTClient, authenticated, make_client, run

app = typer.Typer(help="Authentication and profile.", no_args_is_help=True)


@app.command()
def login(
    email: str = typer.Option(None, "--email", "-e", help="YPT account email."),
    password: str = typer.Option(None, "--password", "-p", help="YPT account password."),
    language: str = typer.Option("en", "--language", "-l", help="Response language."),
) -> None:
    """Log in and cache the session token for future commands."""
    write_template()
    cfg = load_config()
    if not email:
        email = cfg.email or typer.prompt("Email")
    if not password:
        password = cfg.password or getpass.getpass("Password: ")

    async def _impl() -> None:
        with console.status("Logging in..."):
            client = make_client()
            resp = await client.auth.login(email, password, language=language)
            await client.close()
        write_credentials(email, password)
        body = (
            f"Nickname: [bold]{resp.nickname}[/]\n"
            f"Category: {resp.category_code or '-'}\n"
            "Token cached to disk."
        )
        console.print(Panel(body, title="Logged in", border_style="green", padding=(1, 2)))

    run(_impl)


@app.command()
def profile() -> None:
    """Show your profile and today's study summary."""

    async def _impl(client: YPTClient) -> None:
        with console.status("Loading profile..."):
            resp = await client.auth.reload_info()
            day = await client.logs.day(date.today().strftime("%Y-%m-%d"))
        body = f"Nickname: [bold]{resp.nickname}[/]\nCategory: {resp.category_code or '-'}"
        console.print(Panel(body, title="Profile", border_style="cyan", padding=(1, 2)))
        if resp.subjects:
            rows = [(s.title, s.study_ms) for s in resp.subjects if not s.archived]
            console.print(make_subject_table(rows))
        _print_day_summary(day)

    authenticated(_impl)()


def _print_day_summary(day: DayLog) -> None:
    body = f"[green]{format_ms(day.study_ms)}[/] study    [blue]{format_ms(day.rest_ms)}[/] rest"
    console.print(Panel(body, title="Today", border_style="cyan", padding=(0, 2)))