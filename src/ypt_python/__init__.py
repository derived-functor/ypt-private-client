from ypt_python._exceptions import APIError, AuthenticationError, ServerError, YPTError
from ypt_python._models import (
    CategoryRank,
    CategoryRankList,
    DayLog,
    Group,
    GroupMember,
    LoginResponse,
    RankMember,
    Subject,
    SubjectLogEntry,
)
from ypt_python._token_cache import TokenCache
from ypt_python.client import YPTClient

try:
    from ypt_python.cli.app import main
except ImportError:  # pragma: no cover - CLI deps not installed
    main = None  # type: ignore[assignment]

__all__ = [
    "APIError",
    "AuthenticationError",
    "CategoryRank",
    "CategoryRankList",
    "YPTClient",
    "DayLog",
    "Group",
    "GroupMember",
    "LoginResponse",
    "RankMember",
    "ServerError",
    "Subject",
    "SubjectLogEntry",
    "YPTError",
    "TokenCache",
    "main",
]