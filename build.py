#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Gera docs/index.html a partir de SPEC.md.

Uso: python3 build.py
Requer: pip install markdown
"""
import re
import html as htmlmod
from pathlib import Path

import markdown

ROOT = Path(__file__).parent
SRC = ROOT / "SPEC.md"
OUT = ROOT / "docs" / "index.html"

text = SRC.read_text(encoding="utf-8")

# --- 1. Extrai o bloco de metadados (tabela logo após o subtítulo) ---------
meta = {}
lines = text.splitlines()
body_lines = []
in_meta = False
for ln in lines:
    if ln.startswith("| ") and "|---" not in ln and not in_meta and re.match(r"^\| (Versão|Status|Data|Autor|URL canônica|DOI|Licença|Repositório) \|", ln):
        in_meta = True
    if in_meta:
        if ln.strip() == "":
            in_meta = False
            body_lines.append(ln)
            continue
        m = re.match(r"^\| (.+?) \| (.+?) \|$", ln)
        if m and m.group(1).strip() not in ("", "---"):
            meta[m.group(1).strip()] = m.group(2).strip()
        continue
    body_lines.append(ln)

body_md = "\n".join(body_lines)
# remove a linha "| | |" e "|---|---|" residuais do cabeçalho vazio da tabela
body_md = re.sub(r"^\| \| \|\n\|---\|---\|\n", "", body_md, flags=re.M)
# remove título e subtítulo (vão para o hero)
body_md = re.sub(r"^# Workloop Spec\n\n\*\*Especificação do Workloop Agêntico\*\*\n\n", "", body_md)

# --- 2. Markdown -> HTML ----------------------------------------------------
md = markdown.Markdown(extensions=["tables", "toc", "attr_list", "sane_lists"], extension_configs={"toc": {"toc_depth": "2"}})
body_html = md.convert(body_md)
toc_html = md.toc

# --- 3. Realce de identificadores e palavras-chave normativas (fora de <code>) --
ID_RE = re.compile(r"(?<![\w-])((?:DEF|INV|COR|REQ|OPEN|CONF)-(?:\d+|[LSD]))(?![\w-])")
KW_RE = re.compile(r"(?<![\wÀ-ÿ])(NÃO DEVERIA|NÃO DEVEM|NÃO DEVE|DEVERIA|DEVEM|DEVE|PODEM|PODE)(?![\wÀ-ÿ])")

def decorate(seg: str) -> str:
    seg = ID_RE.sub(r'<code class="id">\1</code>', seg)
    seg = KW_RE.sub(r'<span class="kw">\1</span>', seg)
    return seg

parts = re.split(r"(<code>.*?</code>|<pre>.*?</pre>|<h[1-6][^>]*>.*?</h[1-6]>|<[^>]+>)", body_html, flags=re.S)
out = []
for part in parts:
    if not part:
        continue
    if part.startswith("<"):
        out.append(part)  # tags, code, headings ficam intactos
    else:
        out.append(decorate(part))
body_html = "".join(out)

# --- 4. Template ------------------------------------------------------------
def esc(x: str) -> str:
    return htmlmod.escape(x, quote=True)

VERSION = meta.get("Versão", "")
STATUS = meta.get("Status", "")
DATE = meta.get("Data", "")
AUTHOR = meta.get("Autor", "")
URL = meta.get("URL canônica", "")
DOI = meta.get("DOI", "")
LICENSE = meta.get("Licença", "")
REPO = meta.get("Repositório", "")

def linkify(v: str) -> str:
    m = re.search(r"https?://\S+", v)
    if not m:
        return esc(v)
    u = m.group(0)
    return esc(v).replace(esc(u), f'<a href="{esc(u)}">{esc(u)}</a>')

meta_items = [("Versão", VERSION), ("Status", STATUS), ("Data", DATE), ("Autor", AUTHOR),
              ("Licença", LICENSE), ("DOI", DOI), ("URL canônica", URL), ("Repositório", REPO)]
meta_html = "".join(f'<div class="meta-item"><dt>{esc(k)}</dt><dd>{linkify(v)}</dd></div>' for k, v in meta_items if v)

sig_version = VERSION.split(" ")[0].upper()

template = (ROOT / "template.html").read_text(encoding="utf-8")
page = (template
    .replace("{{META_DL}}", meta_html)
    .replace("{{TOC}}", '<div class="toc">\n' + toc_html.split('<div class="toc">',1)[1] if '<div class="toc">' in toc_html else toc_html)
    .replace("{{BODY}}", body_html)
    .replace("{{VER_SHORT}}", sig_version.lower())
    .replace("{{VER}}", VERSION.split(" ")[0])
    .replace("{{VER_UPPER}}", sig_version)
)

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(page, encoding="utf-8")
print(f"ok -> {OUT} ({len(page)} bytes) meta={list(meta.keys())}")
