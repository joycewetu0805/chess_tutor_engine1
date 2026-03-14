#!/usr/bin/env python3
import os
import uvicorn


def _parse_bool(value: str, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


if __name__ == "__main__":
    print("Starting Chess Tutor Engine Backend...")

    port = int(os.getenv("PORT", "8000"))

    # Dev-friendly default, but avoid reload on typical production platforms.
    default_reload = port == 8000 and "RENDER" not in os.environ
    reload = _parse_bool(os.getenv("UVICORN_RELOAD"), default_reload)

    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=reload)
