"""Gera plugins/portal-abono/CATALOG.md a partir do frontmatter das skills e agentes.

Uso:
  python scripts/skills/build_catalog.py          # escreve o catálogo
  python scripts/skills/build_catalog.py --check  # falha (código 1) se estiver desatualizado
Saída determinística: ordenada e sem datas, para diff limpo em PR.
"""
from __future__ import annotations

import sys

from _common import AGENTS_DIR, CATALOG_PATH, CATEGORIES, REPO_ROOT, iter_skills, parse_frontmatter

CATEGORY_TITLES = {
    "explore": "Explorar: entender código, intenção e impacto",
    "review": "Revisar: checklists de revisão",
    "implement": "Implementar: padrões do projeto",
    "verify": "Verificar: execução de build e testes",
    "document": "Documentar: manter a base de conhecimento",
    "explain": "Explicar: ensino e onboarding",
    "domain": "Domínio: casos específicos do negócio",
}


def _cell(text: str) -> str:
    return " ".join(text.replace("|", "\\|").split())


def render() -> str:
    out = [
        "# Catálogo do plugin portal-abono",
        "",
        "> Arquivo GERADO por `scripts/skills/build_catalog.py`. Não edite à mão.",
        "",
        "## Agentes",
        "",
        "| Agente | Descrição |",
        "|---|---|",
    ]
    for path in sorted(AGENTS_DIR.glob("*.agent.md")):
        parsed = parse_frontmatter(path.read_text(encoding="utf-8"))
        desc = parsed[0].get("description", "") if parsed else ""
        out.append(f"| `{path.name[:-len('.agent.md')]}` | {_cell(desc)} |")

    by_cat: dict[str, list] = {c: [] for c in CATEGORIES}
    for category, skill_dir in iter_skills():
        parsed = parse_frontmatter((skill_dir / "SKILL.md").read_text(encoding="utf-8"))
        if not parsed:
            continue
        fm = parsed[0]
        meta = fm.get("metadata") if isinstance(fm.get("metadata"), dict) else {}
        by_cat.setdefault(category, []).append((fm.get("name", skill_dir.name), fm.get("description", ""), meta))

    out += ["", "## Skills", ""]
    total = 0
    for category in CATEGORIES:
        items = sorted(by_cat.get(category, []), key=lambda x: x[0])
        out += [f"### {CATEGORY_TITLES.get(category, category)}", ""]
        if not items:
            out += ["_Nenhuma skill ainda._", ""]
            continue
        out += ["| Skill | Papéis | Dono | Versão | Descrição |", "|---|---|---|---|---|"]
        for name, desc, meta in items:
            out.append(
                f"| `{name}` | {_cell(meta.get('roles', ''))} | {_cell(meta.get('owner', ''))} "
                f"| {_cell(meta.get('version', ''))} | {_cell(desc)} |"
            )
            total += 1
        out.append("")
    out.append(f"Total: {total} skills.")
    return "\n".join(out) + "\n"


def main() -> int:
    content = render()
    if "--check" in sys.argv:
        current = CATALOG_PATH.read_text(encoding="utf-8") if CATALOG_PATH.exists() else ""
        if current != content:
            print(f"CATALOG desatualizado: rode python scripts/skills/build_catalog.py")
            return 1
        print("CATALOG atualizado.")
        return 0
    CATALOG_PATH.write_text(content, encoding="utf-8", newline="\n")
    print(f"Escrito {CATALOG_PATH.relative_to(REPO_ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
