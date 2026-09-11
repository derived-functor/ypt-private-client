"""User configuration stored in ~/.config/ypt-python/config.toml."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore[no-redef]

_DEFAULT_CONFIG_DIR = Path("~/.config/ypt-python").expanduser()
_DEFAULT_CONFIG_PATH = _DEFAULT_CONFIG_DIR / "config.toml"

_TEMPLATE = """\
# ypt-python configuration
# Fill in your YPT account credentials.

[email]
address = ""
password = ""
"""


def config_path() -> Path:
    return _DEFAULT_CONFIG_PATH


def write_template(path: Path = _DEFAULT_CONFIG_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(_TEMPLATE, encoding="utf-8")


@dataclass
class Config:
    email: str = ""
    password: str = ""
    extra: dict[str, object] = field(default_factory=dict)

    def is_authenticated_config(self) -> bool:
        return bool(self.email and self.password)


def load_config(path: Path = _DEFAULT_CONFIG_PATH) -> Config:
    if not path.exists():
        return Config()
    with path.open("rb") as f:
        data = tomllib.load(f)
    email = data.get("email", {})
    return Config(
        email=str(email.get("address", "")),
        password=str(email.get("password", "")),
        extra=data,
    )


def save_config(
    config: dict[str, object] | None = None,
    path: Path = _DEFAULT_CONFIG_PATH,
) -> None:
    data = config if config is not None else _load_existing()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        _dump_toml(data, f)


def _load_existing() -> dict[str, object]:
    cfg = load_config()
    email = {"address": cfg.email, "password": cfg.password}
    return {"email": email, **cfg.extra}


def _dump_toml(data: dict[str, object], f) -> None:
    for section, values in data.items():
        if isinstance(values, dict):
            f.write(f"[{section}]\n")
            for key, value in values.items():
                f.write(f"{key} = {value!r}\n")
            f.write("\n")
        else:
            f.write(f"{section} = {values!r}\n")


def write_credentials(email: str, password: str, path: Path = _DEFAULT_CONFIG_PATH) -> None:
    cfg = _load_existing()
    cfg["email"] = {"address": email, "password": password}
    save_config(cfg, path)