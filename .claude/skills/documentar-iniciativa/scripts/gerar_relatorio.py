#!/usr/bin/env python3
"""
Gera o relatório LaTeX de um card fechado do InovaDados.

    python3 gerar_relatorio.py <pasta-do-card> [-o <saida>] [--subtitulo "Inovação 2026.2"]

Lê `materials/card.md`, `artefatos/resumoexecutivo.md`, `artefatos/benchmarks/<primeiro-nome>-bench.md`
e `artefatos/discovery/<FRAMEWORK>.md`,
converte cada um para LaTeX e monta a árvore de saída:

    <saida>/relatorio.tex
    <saida>/secoes/{resumoexecutivo,introducao,atas,frameworks}.tex
    <saida>/assets/polijunior.png

Não compila. O .tex é o fonte; o PDF é saída derivada (ver README do repo).
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

# --------------------------------------------------------------------------
# leitura de markdown
# --------------------------------------------------------------------------

FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def ler_documento(caminho: Path):
    """Devolve (frontmatter: dict, corpo: str). Tolera arquivo sem `---`."""
    texto = caminho.read_text(encoding="utf-8")
    m = FRONTMATTER.match(texto)
    if not m:
        return {}, texto
    meta = {}
    for linha in m.group(1).splitlines():
        if not linha.strip() or linha.lstrip().startswith("#"):
            continue
        if ":" not in linha:
            continue
        chave, _, valor = linha.partition(":")
        meta[chave.strip()] = valor.strip()
    return meta, texto[m.end():]


def secao_markdown(corpo: str, titulo: str):
    """Extrai o bloco sob um heading `# titulo` / `## titulo` (case-insensitive)."""
    padrao = re.compile(
        r"^#{1,6}\s*" + re.escape(titulo) + r"\s*$(.*?)(?=^#{1,6}\s|\Z)",
        re.MULTILINE | re.DOTALL | re.IGNORECASE,
    )
    m = padrao.search(corpo)
    return m.group(1).strip() if m else ""


def remover_secao(corpo: str, titulo: str):
    """Remove um bloco `# titulo` inteiro, incluindo o heading."""
    padrao = re.compile(
        r"^#{1,6}\s*" + re.escape(titulo) + r"\s*$.*?(?=^#{1,6}\s|\Z)",
        re.MULTILINE | re.DOTALL | re.IGNORECASE,
    )
    return padrao.sub("", corpo)


ROTULO_CARD = re.compile(r"^[^\s:][^:\n]{0,60}:\s")


def campo_card(corpo: str, rotulo: str):
    """Lê um campo `Rotulo: valor` do card.md, aceitando valor multilinha.

    Parsing por linha, não por regex sobre o texto todo: um `.*?` com DOTALL
    atravessa a quebra de linha e casa com o `:` do campo seguinte, truncando
    o valor na primeira linha.
    """
    linhas = corpo.splitlines()
    inicio = re.compile(r"^" + re.escape(rotulo) + r"\s*:\s*(.*)$", re.IGNORECASE)

    for i, linha in enumerate(linhas):
        m = inicio.match(linha)
        if not m:
            continue
        partes = [m.group(1).strip()]
        for seguinte in linhas[i + 1:]:
            # o valor termina na linha em branco, no próximo heading ou no
            # próximo campo `Rotulo:` do card
            if not seguinte.strip() or seguinte.lstrip().startswith("#") \
                    or ROTULO_CARD.match(seguinte):
                break
            partes.append(seguinte.strip())
        valor = " ".join(p for p in partes if p).strip()
        # placeholder não preenchido do template
        if re.fullmatch(r"<[^>]*>", valor):
            return ""
        return valor
    return ""


# --------------------------------------------------------------------------
# conversão markdown -> latex
# --------------------------------------------------------------------------

NIVEIS = ["section", "subsection", "subsubsection", "paragraph", "subparagraph"]

ESCAPES = {
    "\\": r"\textbackslash{}",
    "{": r"\{",
    "}": r"\}",
    "$": r"\$",
    "&": r"\&",
    "#": r"\#",
    "%": r"\%",
    "_": r"\_",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


def escapar(texto: str) -> str:
    return "".join(ESCAPES.get(c, c) for c in texto)


def inline(texto: str) -> str:
    """Converte ênfase, código e links; escapa o resto."""
    partes = []
    padrao = re.compile(
        r"`([^`]+)`"                      # código
        r"|\[([^\]]+)\]\(([^)]+)\)"       # link
        r"|\*\*([^*]+)\*\*"               # negrito
        r"|(?<!\*)\*([^*]+)\*(?!\*)"      # itálico
    )
    pos = 0
    for m in padrao.finditer(texto):
        partes.append(escapar(texto[pos:m.start()]))
        codigo, rotulo, url, negrito, italico = m.groups()
        if codigo is not None:
            partes.append(r"\texttt{" + escapar(codigo) + "}")
        elif rotulo is not None:
            partes.append(r"\href{" + url.replace("%", r"\%").replace("#", r"\#")
                          + "}{" + inline(rotulo) + "}")
        elif negrito is not None:
            partes.append(r"\textbf{" + inline(negrito) + "}")
        else:
            partes.append(r"\emph{" + inline(italico) + "}")
        pos = m.end()
    partes.append(escapar(texto[pos:]))
    return "".join(partes)


def md_para_latex(corpo: str, nivel_base: int = 0) -> str:
    """Converte um corpo markdown. `nivel_base` desloca os headings."""
    corpo = re.sub(r"<!--.*?-->", "", corpo, flags=re.DOTALL)
    saida, buffer_par, lista_aberta, em_codigo = [], [], None, False

    def fechar_paragrafo():
        if buffer_par:
            saida.append(inline(" ".join(buffer_par)))
            saida.append("")
            buffer_par.clear()

    def fechar_lista():
        nonlocal lista_aberta
        if lista_aberta:
            saida.append(r"\end{" + lista_aberta + "}")
            saida.append("")
            lista_aberta = None

    for linha in corpo.splitlines():
        if linha.strip().startswith("```"):
            fechar_paragrafo(); fechar_lista()
            saida.append(r"\end{verbatim}" if em_codigo else r"\begin{verbatim}")
            em_codigo = not em_codigo
            continue
        if em_codigo:
            saida.append(linha)
            continue

        cabecalho = re.match(r"^(#{1,6})\s+(.*)$", linha)
        if cabecalho:
            fechar_paragrafo(); fechar_lista()
            idx = min(len(cabecalho.group(1)) - 1 + nivel_base, len(NIVEIS) - 1)
            titulo = inline(cabecalho.group(2).strip())
            cmd = NIVEIS[idx]
            saida.append("\\" + cmd + "{" + titulo + "}"
                         + ("" if idx < 3 else r"\quad"))
            saida.append("")
            continue

        item = re.match(r"^\s*[-*+]\s+(?:\[[ xX]\]\s*)?(.*)$", linha)
        numerado = re.match(r"^\s*\d+[.)]\s+(.*)$", linha)
        if item or numerado:
            fechar_paragrafo()
            alvo = "itemize" if item else "enumerate"
            conteudo = (item or numerado).group(1).strip()
            if lista_aberta != alvo:
                fechar_lista()
                saida.append(r"\begin{" + alvo + "}")
                lista_aberta = alvo
            if not conteudo:          # bullet vazio do template
                continue
            saida.append(r"  \item " + inline(conteudo))
            continue

        if not linha.strip():
            fechar_paragrafo(); fechar_lista()
            continue

        if lista_aberta:              # continuação de item
            saida[-1] = saida[-1].rstrip() + " " + inline(linha.strip())
            continue

        buffer_par.append(linha.strip())

    if em_codigo:
        saida.append(r"\end{verbatim}")
    fechar_paragrafo(); fechar_lista()
    return "\n".join(saida).strip() + "\n"


# --------------------------------------------------------------------------
# montagem das seções
# --------------------------------------------------------------------------

def bloco_metadados(meta: dict, chaves) -> str:
    itens = []
    for chave in chaves:
        valor = meta.get(chave, "").strip()
        if valor and not re.fullmatch(r"<.*>", valor):
            itens.append(r"\textbf{" + escapar(chave) + ":} " + inline(valor))
    if not itens:
        return ""
    return "\\metadados{" + r" \\ ".join(itens) + "}\n\n"


def achar_doc(pasta: Path, *relativos):
    """Primeiro caminho existente, na ordem dada.

    O layout da iniciativa separa insumo (`materials/`) de produto
    (`artefatos/`); o caminho solto na raiz fica como fallback para as pastas
    criadas antes dessa separacao.
    """
    for rel in relativos:
        caminho = pasta / rel
        if caminho.exists():
            return caminho
    return None


def gerar_resumo(pasta: Path, avisos):
    caminho = achar_doc(pasta, "artefatos/resumoexecutivo.md", "resumoexecutivo.md")
    if caminho is None:
        avisos.append(
            "artefatos/resumoexecutivo.md não encontrado — card não está fechado.")
        return "\\section{Resumo Executivo}\n\n\\emph{Resumo executivo ausente.}\n"
    _, corpo = ler_documento(caminho)
    corpo = corpo.strip()
    if not re.match(r"^#\s", corpo):
        corpo = "# Resumo Executivo\n\n" + corpo
    texto = md_para_latex(corpo, 0)
    palavras = len(re.findall(r"\w+", re.sub(r"^#.*$", "", corpo, flags=re.MULTILINE)))
    if palavras > 100:
        avisos.append(f"Resumo executivo com {palavras} palavras (limite do template: 100).")
    return texto


def gerar_introducao(pasta: Path, raiz: Path, meta_card: dict, corpo_card: str,
                     iniciativa: str, avisos):
    local = achar_doc(pasta, "artefatos/introducao.md", "introducao.md")
    modelo = local or achar_template(raiz, "introducao.md")
    if modelo is None or not modelo.exists():
        avisos.append("templates/introducao.md não encontrado — introdução omitida.")
        return ""
    _, corpo = ler_documento(modelo)
    # o template documenta os marcadores em um comentário HTML; removê-lo antes
    # da substituição evita "preencher" a própria documentação
    corpo = re.sub(r"<!--.*?-->", "", corpo, flags=re.DOTALL)

    substituicoes = {
        "iniciativa": iniciativa,
        "ciclo": meta_card.get("ciclo", ""),
        "nucleo": meta_card.get("nucleo", ""),
        "porque": campo_card(corpo_card, "Por quê") or campo_card(corpo_card, "Por que"),
        "objetivo": campo_card(corpo_card, "Objetivo deste card")
                    or campo_card(corpo_card, "Objetivo"),
        "metricas": campo_card(corpo_card, "Métricas de Sucesso"),
    }

    def trocar(m):
        chave = m.group(1).strip()
        valor = substituicoes.get(chave, "").strip()
        if not valor:
            avisos.append(f"Introdução: marcador {{{{{chave}}}}} sem valor no card.md.")
            return f"**[preencher: {chave}]**"
        return valor

    corpo = re.sub(r"\{\{([^}]+)\}\}", trocar, corpo)
    return md_para_latex(corpo, 0)


def gerar_atas(pasta: Path, avisos):
    dir_atas = achar_doc(pasta, "artefatos/benchmarks", "benchmarks")
    # A ata é nomeada pelo entrevistado (`<primeiro-nome>-bench.md`), então a
    # ordem alfabética do arquivo não é a ordem de ID que o relatório promete.
    # Ordena pelo `id` do frontmatter, caindo no nome só se o id faltar.
    arquivos = sorted(dir_atas.glob("*-bench.md")) if dir_atas else []
    arquivos.sort(key=lambda c: (ler_documento(c)[0].get("id") or c.stem))
    if not arquivos:
        avisos.append("Nenhuma ata em artefatos/benchmarks/ — seção de atas omitida.")
        return ""

    # Cada ata é uma \section própria, iniciando em página nova: ela é um
    # artefato independente e precisa aparecer assim no sumário. Agrupá-las sob
    # uma seção comum faria "# Perguntas" virar irmão do título da ata.
    partes = []
    for caminho in arquivos:
        meta, corpo = ler_documento(caminho)
        if re.search(r"^#\s*Rascunho\s*$", corpo, re.MULTILINE | re.IGNORECASE):
            rascunho = secao_markdown(corpo, "Rascunho")
            if rascunho:
                avisos.append(
                    f"{caminho.name}: seção '# Rascunho' com conteúdo — "
                    "card fechado não deveria ter rascunho. Omitida do relatório.")
            corpo = remover_secao(corpo, "Rascunho")

        ident = meta.get("id") or caminho.stem
        entrevistado = meta.get("entrevistado", "").strip()
        titulo = f"Ata {ident} — {entrevistado}" if entrevistado else f"Ata {ident}"
        partes.append("\\clearpage")
        partes.append("\\section{" + inline(titulo) + "}")
        partes.append("")
        partes.append(bloco_metadados(
            meta, ["entrevistado", "entrevistador", "data", "link (Call)", "link (Notion)"]))
        partes.append(md_para_latex(corpo, 1))
        partes.append("")
    return "\n".join(partes)


def gerar_frameworks(pasta: Path, avisos):
    dir_fw = achar_doc(pasta, "artefatos/discovery", "discovery")
    # O framework é nomeado pelo próprio nome (`CSD.md`, `SWOT.md`), sem prefixo
    # comum para filtrar — pega todo .md da pasta e ordena pelo `id`.
    arquivos = sorted(dir_fw.glob("*.md")) if dir_fw else []
    arquivos.sort(key=lambda c: (ler_documento(c)[0].get("id") or c.stem))
    if not arquivos:
        avisos.append(
            "Nenhum framework em artefatos/discovery/ — seção de frameworks omitida.")
        return ""

    partes = []
    for caminho in arquivos:
        meta, corpo = ler_documento(caminho)
        ident = meta.get("id") or caminho.stem
        tipo = meta.get("tipo", "").strip()

        if not meta.get("origem", "").strip():
            avisos.append(f"{caminho.name}: sem campo 'origem' — análise não rastreável.")

        # o H1 do template ("# Matriz CSD") vira o título da subseção
        cabecalho = re.match(r"^\s*#\s+(.*)$", corpo, re.MULTILINE)
        rotulo = cabecalho.group(1).strip() if cabecalho else (tipo or ident)
        corpo = re.sub(r"^\s*#\s+.*$", "", corpo, count=1, flags=re.MULTILINE)

        partes.append("\\clearpage")
        partes.append("\\section{" + inline(f"{rotulo} ({ident})") + "}")
        partes.append("")
        partes.append(bloco_metadados(meta, ["tipo", "origem", "link (Notion)"]))
        partes.append(md_para_latex(corpo, 1))
        partes.append("")
    return "\n".join(partes)


# --------------------------------------------------------------------------

def achar_template(raiz: Path, *nomes):
    """Localiza um arquivo sob templates/, tolerando aninhamento (templates/templates/).

    A pasta templates/ do repositório já apareceu em dois layouts; procurar em vez
    de fixar o caminho evita que o gerador quebre quando alguém a reorganiza.
    """
    base = raiz / "templates"
    for nome in nomes:
        direto = base / nome
        if direto.exists():
            return direto
    for nome in nomes:
        achados = sorted(base.rglob(nome))
        if achados:
            return achados[0]
    return None


def achar_raiz(pasta: Path) -> Path:
    for candidato in [pasta, *pasta.parents]:
        if (candidato / "README.md").exists() and (candidato / "templates").is_dir():
            return candidato
    raise SystemExit("ERRO: raiz do repositório InovaDados não encontrada "
                     "(README.md + templates/ ausentes nos diretórios acima).")


def nome_iniciativa(pasta: Path, meta_card: dict, corpo_card: str) -> str:
    cabecalho = re.match(r"^\s*#\s+(.*)$", corpo_card, re.MULTILINE)
    if cabecalho and not re.fullmatch(r"<.*>", cabecalho.group(1).strip()):
        return cabecalho.group(1).strip()
    partes = pasta.resolve().parts
    if "iniciativas" in partes:
        slug = partes[partes.index("iniciativas") + 1]
        return slug.replace("-", " ").title()
    return pasta.name.replace("-", " ").title()


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("card", type=Path, help="pasta do card fechado")
    ap.add_argument("-o", "--saida", type=Path, default=None,
                    help="diretório de saída (padrão: <card>/relatorio)")
    ap.add_argument("--subtitulo", default=None,
                    help='subtítulo da capa (padrão: "Inovação <ciclo>")')
    ap.add_argument("--titulo", default=None, help="sobrescreve o nome da iniciativa")
    args = ap.parse_args()

    pasta = args.card.expanduser().resolve()
    if not pasta.is_dir():
        raise SystemExit(f"ERRO: {pasta} não é uma pasta.")
    raiz = achar_raiz(pasta)
    avisos = []

    caminho_card = achar_doc(pasta, "materials/card.md", "card.md")
    if caminho_card is None:
        raise SystemExit(
            f"ERRO: {pasta / 'materials' / 'card.md'} não existe — "
            "isso não é a pasta de um card.")
    meta_card, corpo_card = ler_documento(caminho_card)

    logo = achar_template(raiz, "logo-polijunior.png", "logo-polijunior.pdf",
                          "logo-polijunior.jpg")
    if logo is None:
        raise SystemExit(
            "ERRO: marca d'água ausente.\n"
            f"  Esperado: {raiz / 'templates' / 'logo-polijunior.png'} (ou .pdf/.jpg)\n"
            "  Veja templates/latex/LEIA-ME.md.")

    iniciativa = args.titulo or nome_iniciativa(pasta, meta_card, corpo_card)
    ciclo = meta_card.get("ciclo", "").strip()
    subtitulo = args.subtitulo or (f"Inovação {ciclo}" if ciclo else "Inovação")
    if not ciclo and not args.subtitulo:
        avisos.append("card.md sem 'ciclo' — subtítulo da capa ficou sem o semestre.")

    saida = (args.saida or pasta / "relatorio").expanduser().resolve()
    (saida / "secoes").mkdir(parents=True, exist_ok=True)
    (saida / "assets").mkdir(parents=True, exist_ok=True)
    shutil.copy2(logo, saida / "assets" / logo.name)

    secoes = {
        "resumoexecutivo": gerar_resumo(pasta, avisos),
        "introducao": gerar_introducao(pasta, raiz, meta_card, corpo_card,
                                       iniciativa, avisos),
        "atas": gerar_atas(pasta, avisos),
        "frameworks": gerar_frameworks(pasta, avisos),
    }
    cabecalho = ("% Gerado por .claude/skills/documentar-iniciativa — NÃO EDITE À MÃO.\n"
                 "% A fonte é o markdown do card; regenere após alterá-lo.\n\n")
    for nome, conteudo in secoes.items():
        destino = saida / "secoes" / f"{nome}.tex"
        if nome in ("resumoexecutivo", "introducao"):
            conteudo = "\\clearpage\n" + conteudo if nome == "introducao" else conteudo
        destino.write_text(cabecalho + (conteudo or "% seção vazia\n"), encoding="utf-8")

    caminho_modelo = achar_template(raiz, "relatorio.tex")
    if caminho_modelo is None:
        raise SystemExit("ERRO: templates/latex/relatorio.tex não encontrado.")
    modelo = caminho_modelo.read_text(encoding="utf-8")
    modelo = (modelo
              .replace("<<INICIATIVA>>", escapar(iniciativa))
              .replace("<<SUBTITULO>>", escapar(subtitulo))
              .replace("<<LOGO>>", "assets/" + logo.name))
    (saida / "relatorio.tex").write_text(modelo, encoding="utf-8")

    print(f"Gerado: {saida / 'relatorio.tex'}")
    print(f"Iniciativa: {iniciativa}")
    print(f"Subtítulo:  {subtitulo}")
    for nome, conteudo in secoes.items():
        estado = f"{len(conteudo.splitlines())} linhas" if conteudo else "vazia"
        print(f"  secoes/{nome}.tex — {estado}")
    if avisos:
        print("\nAvisos:", file=sys.stderr)
        for aviso in avisos:
            print(f"  - {aviso}", file=sys.stderr)


if __name__ == "__main__":
    main()
