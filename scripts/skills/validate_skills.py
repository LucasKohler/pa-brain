"""Valida as skills e os agentes do plugin portal-abono.

Uso: python scripts/skills/validate_skills.py
Sai com código 1 se houver erro. Avisos não falham.
"""
from __future__ import annotations

import json
import sys

from _common import (AGENTS_DIR, CATEGORIES, NAME_RE, PLUGIN_DIR, REPO_ROOT, ROLES,
                     SKILLS_DIR, iter_skills, parse_frontmatter)

REQUIRED_METADATA = ["category", "roles", "owner", "version", "origin"]
SUSPICIOUS = ["ignore as regras", "ignore previous", "ignore all previous", "desconsidere as instruções"]


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    def rel(p):
        return p.relative_to(REPO_ROOT).as_posix()

    # plugin.json: pastas de skills declaradas = categorias existentes
    manifest = json.loads((PLUGIN_DIR / "plugin.json").read_text(encoding="utf-8"))
    declared = {s.strip("/").split("/")[-1] for s in manifest.get("skills", [])}
    existing = {p.name for p in SKILLS_DIR.iterdir() if p.is_dir()}
    for cat in sorted(existing - set(CATEGORIES)):
        errors.append(f"skills/{cat}: categoria desconhecida (válidas: {', '.join(CATEGORIES)})")
    for cat in sorted(existing - declared):
        errors.append(f"plugin.json: pasta skills/{cat}/ existe mas não está declarada em 'skills'")
    for cat in sorted(declared - existing):
        errors.append(f"plugin.json: 'skills/{cat}/' declarada mas a pasta não existe")

    # SKILL.md fora do lugar (o Copilot só lê skills/<categoria>/<nome>/SKILL.md)
    for path in SKILLS_DIR.rglob("SKILL.md"):
        depth = len(path.relative_to(SKILLS_DIR).parts)
        if depth != 3:
            errors.append(f"{rel(path)}: SKILL.md deve estar em skills/<categoria>/<nome>/SKILL.md")

    names: dict[str, str] = {}
    for category, skill_dir in iter_skills():
        path = skill_dir / "SKILL.md"
        parsed = parse_frontmatter(path.read_text(encoding="utf-8"))
        if parsed is None:
            errors.append(f"{rel(path)}: frontmatter ausente ou malformado")
            continue
        fm, body = parsed
        name = fm.get("name", "")
        desc = fm.get("description", "")
        meta = fm.get("metadata") if isinstance(fm.get("metadata"), dict) else {}

        if name != skill_dir.name:
            errors.append(f"{rel(path)}: name '{name}' difere da pasta '{skill_dir.name}'")
        if not NAME_RE.match(name or "") or len(name) > 64:
            errors.append(f"{rel(path)}: name inválido (minúsculas, números e hífens; até 64)")
        if not name.startswith(category + "-"):
            errors.append(f"{rel(path)}: name deve começar com o prefixo da categoria '{category}-'")
        if name in names:
            errors.append(f"{rel(path)}: name duplicado (também em {names[name]})")
        names[name] = rel(path)

        if not (40 <= len(desc) <= 1024):
            errors.append(f"{rel(path)}: description deve ter entre 40 e 1024 caracteres (tem {len(desc)})")
        elif "use " not in desc.lower():
            warnings.append(f"{rel(path)}: description sem gatilho ('Use quando/ao/em ...')")

        for key in REQUIRED_METADATA:
            if not meta.get(key):
                errors.append(f"{rel(path)}: metadata.{key} ausente")
        if meta.get("category") and meta["category"] != category:
            errors.append(f"{rel(path)}: metadata.category '{meta['category']}' difere da pasta '{category}'")
        roles = {r.strip() for r in meta.get("roles", "").split(",") if r.strip()}
        if roles - ROLES:
            errors.append(f"{rel(path)}: roles desconhecidos {sorted(roles - ROLES)} (válidos: {sorted(ROLES)})")

        if len(body.splitlines()) > 500:
            warnings.append(f"{rel(path)}: corpo longo; mova detalhes para references/")
        low = body.lower()
        for s in SUSPICIOUS:
            if s in low:
                errors.append(f"{rel(path)}: texto suspeito de injeção de instrução: '{s}'")

    # Agentes
    agent_files = sorted(AGENTS_DIR.glob("*.agent.md"))
    if not agent_files:
        warnings.append("nenhum agente em plugins/portal-abono/agents/")
    for path in agent_files:
        parsed = parse_frontmatter(path.read_text(encoding="utf-8"))
        if parsed is None:
            errors.append(f"{rel(path)}: frontmatter ausente ou malformado")
            continue
        fm, body = parsed
        agent_id = path.name[: -len(".agent.md")]
        if not fm.get("description"):
            errors.append(f"{rel(path)}: description ausente")
        if fm.get("name") and fm["name"] != agent_id:
            errors.append(f"{rel(path)}: name '{fm['name']}' difere do arquivo '{agent_id}'")
        if "PENDENTE" in body or "PENDENTE" in fm.get("description", ""):
            warnings.append(f"{rel(path)}: agente marcado como PENDENTE (não distribuir)")
        for ref in sorted(set(_skill_refs(body))):
            if ref not in names:
                errors.append(f"{rel(path)}: roteia para a skill '{ref}', que não existe")

    for w in warnings:
        print(f"AVISO  {w}")
    for e in errors:
        print(f"ERRO   {e}")
    print(f"\n{len(names)} skills, {len(agent_files)} agentes, {len(errors)} erros, {len(warnings)} avisos.")
    return 1 if errors else 0


def _skill_refs(body: str):
    """Nomes entre crases que parecem skills (prefixo de categoria)."""
    import re
    for m in re.finditer(r"`([a-z0-9-]+)`", body):
        token = m.group(1)
        prefix = token.split("-")[0]
        if prefix in CATEGORIES and "-" in token and not token.endswith("-"):
            if token.startswith("domain-") and token == "domain-":
                continue
            yield token


if __name__ == "__main__":
    sys.exit(main())
