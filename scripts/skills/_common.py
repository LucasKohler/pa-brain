"""Funções compartilhadas pelos scripts de skills (somente biblioteca padrão)."""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PLUGIN_DIR = REPO_ROOT / "plugins" / "portal-abono"
SKILLS_DIR = PLUGIN_DIR / "skills"
AGENTS_DIR = PLUGIN_DIR / "agents"
CATALOG_PATH = PLUGIN_DIR / "CATALOG.md"

CATEGORIES = ["explore", "review", "implement", "verify", "document", "explain", "domain"]
ROLES = {"explorer", "reviewer", "implementer", "tester", "documenter", "teacher"}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def parse_frontmatter(text: str) -> tuple[dict, str] | None:
    """Lê um frontmatter YAML simples: chaves de 1º nível e um bloco aninhado (ex.: metadata)."""
    text = text.lstrip("﻿")
    if not text.startswith("---"):
        return None
    lines = text.splitlines()
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return None
    data: dict = {}
    current: str | None = None
    for raw in lines[1:end]:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indented = raw.startswith((" ", "\t"))
        key, sep, value = raw.strip().partition(":")
        if not sep:
            continue
        value = _clean(value)
        if indented and current is not None and isinstance(data.get(current), dict):
            data[current][key.strip()] = value
        elif not indented:
            current = key.strip()
            data[current] = {} if value == "" else value
    body = "\n".join(lines[end + 1:])
    return data, body


def _clean(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    return value


def iter_skills():
    """Retorna (categoria, pasta_da_skill) para cada SKILL.md em skills/<categoria>/<nome>/."""
    for category_dir in sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir()):
        for skill_dir in sorted(p for p in category_dir.iterdir() if p.is_dir()):
            if (skill_dir / "SKILL.md").is_file():
                yield category_dir.name, skill_dir
