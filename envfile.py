"""Read and write a subset of dotenv files."""
from __future__ import annotations


def parse_env(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            raise ValueError(f"缺少等号: {line}")
        key, value = line.split("=", 1)
        key = key.strip()
        if not key or any(ch.isspace() for ch in key):
            raise ValueError(f"键不合法: {key}")
        out[key] = _unquote(value.strip())
    return out


def overlay_env(base: dict[str, str], extra: dict[str, str]) -> dict[str, str]:
    merged = dict(base)
    merged.update(extra)
    for key in merged:
        if not key or any(ch.isspace() for ch in key):
            raise ValueError(f"键不合法: {key}")
    return merged


def emit_env(data: dict[str, str]) -> str:
    lines = []
    for key, value in data.items():
        if not key or any(ch.isspace() for ch in key):
            raise ValueError(f"键不合法: {key}")
        lines.append(f"{key}={_quote(value)}")
    return "\n".join(lines) + ("\n" if lines else "")


def _unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def _quote(value: str) -> str:
    if value == "" or any(ch in value for ch in " #\""):
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    return value
