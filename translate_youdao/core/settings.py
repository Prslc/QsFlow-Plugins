# -*- coding: utf-8 -*-
"""Translate settings from ~/.config/wayrun/translate.toml.

A template is written on first run; credentials missing or unreadable config
mean "not configured" (`load_settings` returns None).
"""
import os
import tomllib

from pathlib import Path

from .lang import LANG_MAP

CONFIG_DIR = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "wayrun"
CONFIG_PATH = CONFIG_DIR / "translate.toml"

CONFIG_TEMPLATE = """\
# Youdao translation plugin
app_token = ""
app_secret = ""

# Optional. Defaults: Auto -> English. Display names: Auto, English,
# Chinese (Simplified), Chinese (Traditional), Japanese, Korean, French,
# German, Spanish, Russian, Portuguese, Italian, Vietnamese, Thai,
# Indonesian, Arabic
# lang_from = "Auto"
# lang_to = "English"
"""


def load_settings():
    if not CONFIG_PATH.exists():
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        try:
            CONFIG_PATH.write_text(CONFIG_TEMPLATE, encoding="utf-8")
        except OSError:
            pass
        return None
    try:
        with CONFIG_PATH.open("rb") as f:
            raw = tomllib.load(f)
    except (OSError, tomllib.TOMLDecodeError):
        return None

    app_token = str(raw.get("app_token", ""))
    app_secret = str(raw.get("app_secret", ""))
    if not app_token or not app_secret:
        return None

    lang_from = str(raw.get("lang_from", "Auto"))
    lang_to = str(raw.get("lang_to", "English"))
    return {
        "app_token": app_token,
        "app_secret": app_secret,
        "lang_from": LANG_MAP.get(lang_from, "auto"),
        "lang_to": LANG_MAP.get(lang_to, "en"),
        "lang_from_display": lang_from,
        "lang_to_display": lang_to,
    }
