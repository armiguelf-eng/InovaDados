#!/usr/bin/env python3
"""
Compara o README.md com o repositório InovaDados e lista as divergências.

    python3 verificar_readme.py [--raiz .]

Não edita nada: aponta. Sai com 1 se houver divergência, 0 se estiver limpo.
A correção é feita pela skill `sincronizar-readme`, com julgamento.
"""

import argparse
import json
import re
import sys
from pathlib import Path

TEMPLATES_IGNORADOS = {".DS_Store"}


def bloco_secao(readme: str, titulo: str) -> str:
    """Devolve o texto sob `## titulo`, até o próximo heading de mesmo nível."""
    padrao = re.compile(
        r"^##\s+" + re.escape(titulo) + r"\s*$(.*?)(?=^##\s|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    m = padrao.search(readme)
    return m.group(1) if m else ""


def tipos_dos_templates(raiz: Path) -> set:
    tipos = set()
    for md in sorted(raiz.glob("templates/**/*.md")):
        for linha in md.read_text(encoding="utf-8").splitlines()[:15]:
            if linha.startswith("tipo:"):
                valor = linha.partition(":")[2].strip()
                if valor:
                    tipos.add(valor)
                break
    return tipos


def templates_reais(raiz: Path) -> set:
    """Caminhos de template relativos a `templates/`, como citados no README."""
    achados = set()
    base = raiz / "templates"
    for caminho in base.rglob("*"):
        if not caminho.is_file() or caminho.name in TEMPLATES_IGNORADOS:
            continue
        if caminho.suffix not in (".md", ".tex"):
            continue
        rel = caminho.relative_to(base).as_posix()
        if rel == "latex/LEIA-ME.md":  # documentação do template, não é template
            continue
        achados.add(rel)
    return achados


def verificar(raiz: Path) -> list:
    readme_path = raiz / "README.md"
    if not readme_path.exists():
        return ["README.md não encontrado na raiz."]

    readme = readme_path.read_text(encoding="utf-8")
    problemas = []

    # --- templates: um por linha da tabela, e vice-versa --------------------
    tabela = bloco_secao(readme, "Templates")
    citados = set(re.findall(r"\|\s*`([^`]+\.(?:md|tex))`", tabela))
    reais = templates_reais(raiz)

    for faltando in sorted(reais - citados):
        problemas.append(
            f"templates/{faltando} existe mas não está na tabela `## Templates`."
        )
    for sobrando in sorted(citados - reais):
        problemas.append(
            f"A tabela `## Templates` cita `{sobrando}`, que não existe em templates/."
        )

    # --- vocabulário de `tipo:` --------------------------------------------
    m = re.search(r"^tipo:\s*(.+)$", readme, re.MULTILINE)
    if m:
        declarados = {t.strip() for t in m.group(1).split("|") if t.strip()}
        usados = tipos_dos_templates(raiz)
        for t in sorted(usados - declarados):
            problemas.append(
                f"`tipo: {t}` é usado em templates/ mas não está listado em `## Frontmatter`."
            )
        for t in sorted(declarados - usados):
            problemas.append(
                f"`## Frontmatter` declara `tipo: {t}`, que nenhum template usa."
            )
    else:
        problemas.append("Não achei a linha `tipo:` no bloco de frontmatter do README.")

    # --- caminhos citados em blocos bash existem ---------------------------
    for caminho in re.findall(r"(\.claude/[\w./-]+\.py)", readme):
        if not (raiz / caminho).exists():
            problemas.append(f"O README cita o script `{caminho}`, que não existe.")

    # --- skills documentadas na árvore -------------------------------------
    estrutura = bloco_secao(readme, "Estrutura")
    dir_skills = raiz / ".claude" / "skills"
    if dir_skills.is_dir():
        for skill in sorted(p.name for p in dir_skills.iterdir() if p.is_dir()):
            if skill not in estrutura:
                problemas.append(
                    f"A skill `{skill}` existe mas não aparece na árvore de `## Estrutura`."
                )

    # --- iniciativas -------------------------------------------------------
    dir_iniciativas = raiz / "iniciativas"
    existentes = (
        sorted(p.name for p in dir_iniciativas.iterdir() if p.is_dir())
        if dir_iniciativas.is_dir()
        else []
    )
    pendencias = bloco_secao(readme, "Pendências")
    if existentes and "iniciativas/` ainda não existe" in pendencias:
        problemas.append(
            "`## Pendências` diz que não há iniciativa, mas existem: "
            + ", ".join(existentes)
        )

    # frontmatter `card:` bate com o nome da pasta da iniciativa
    for nome in existentes:
        for md in sorted((dir_iniciativas / nome).rglob("*.md")):
            for linha in md.read_text(encoding="utf-8").splitlines()[:15]:
                if linha.startswith("card:"):
                    valor = linha.partition(":")[2].strip()
                    if valor and valor != nome:
                        rel = md.relative_to(raiz).as_posix()
                        problemas.append(
                            f"{rel} tem `card: {valor}`, mas está na pasta `{nome}`."
                        )
                    break

    # --- .gitignore: exceções citadas no README batem ----------------------
    gitignore = raiz / ".gitignore"
    if gitignore.exists():
        conteudo = gitignore.read_text(encoding="utf-8")
        nao_entra = bloco_secao(readme, "Não entra neste repositório")
        for excecao in re.findall(r"`(templates/[\w./-]+)`", nao_entra):
            if excecao.rsplit("/", 1)[-1] not in conteudo:
                problemas.append(
                    f"O README chama `{excecao}` de exceção, mas o .gitignore não a declara."
                )

    return problemas


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--raiz", default=".", type=Path)
    p.add_argument(
        "--hook",
        action="store_true",
        help="modo hook Stop: sempre sai 0, emitindo decision=block em JSON se houver divergência",
    )
    args = p.parse_args()

    raiz = args.raiz.resolve()
    problemas = verificar(raiz)

    if args.hook:
        if not problemas:
            return 0
        lista = "\n".join(f"  - {i}" for i in problemas)
        print(
            json.dumps(
                {
                    "decision": "block",
                    "reason": (
                        "O README.md divergiu do repositório e ainda não foi "
                        f"sincronizado:\n{lista}\n\nUse a skill `sincronizar-readme` "
                        "para corrigir antes de encerrar o turno."
                    ),
                }
            )
        )
        return 0

    if not problemas:
        print("README sincronizado com o repositório.")
        return 0

    print(f"{len(problemas)} divergência(s) entre o README e o repositório:\n")
    for item in problemas:
        print(f"  - {item}")
    print("\nCorrija com a skill `sincronizar-readme`.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
