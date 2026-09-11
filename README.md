# ypt-python

Async Python client for the YPT (열품타) study-time tracking API.

## Installation

```bash
uv add ypt-python
```

## Quick start

Example that only reads data (no timer control) — good for verifying that
credentials and the library work:

```python
import asyncio
from datetime import date

from ypt_python import YPTClient


async def check() -> None:
    async with YPTClient() as client:
        login = await client.auth.login("user@example.com", "password")
        print(f"Logged in as {login.nickname}")

        today = date.today().isoformat()

        day_log = await client.logs.day(today)
        print(f"Today: {day_log.study_hours:.2f}h studied, {day_log.rest_hours:.2f}h rest")

        my_rank = await client.ranks.my_rank(login.category_id, login.country_id)
        print(f"My rank in {login.category_code}: {my_rank}")

        groups = await client.groups.my_groups()
        for g in groups:
            print(f"Group: {g.title} ({g.member_count} members)")


asyncio.run(check())
```

## API overview

| Namespace | Methods | Purpose |
|---|---|---|
| `client.auth` | `login()`, `reload_info()` | Authentication, profile |
| `client.logs` | `day()` | Daily study logs |
| `client.ranks` | `my_rank()`, `category_members()` | Rankings and leaderboards |
| `client.groups` | `browse()`, `my_groups()`, `members()` | Study groups |
| `client.study` | `start()`, `stop()` | Study timer control |

## Error handling

```python
from ypt_python import AuthenticationError, ServerError

try:
    await client.auth.login("user@example.com", "wrong")
except AuthenticationError as e:
    print(f"Auth failed (code {e.code})")
except ServerError:
    print("YPT server is unavailable")
```

## Requirements

- Python >= 3.14
- httpx
- pydantic >= 2.0

## Disclaimer

Unofficial library reverse-engineered from the YPT Android app. Not affiliated
with Pallo Inc.