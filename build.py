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

page = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Workloop Spec · Especificação do Workloop Agêntico</title>
<meta name="description" content="Workloop Spec: especificação do workloop agêntico, sistema de loops agênticos que interagem sob uma autoridade de política, com gates determinísticos na costura. Protocolo AISAC · B2 Tech.">
<meta name="author" content="Bruno Bracaioli">
<meta property="og:title" content="Workloop Spec · Especificação do Workloop Agêntico">
<meta property="og:description" content="Liberdade dentro do loop, determinismo na costura. Termos, invariante, corolários e conformidade do workloop agêntico.">
<meta property="og:type" content="article">
<link rel="canonical" href="{esc(URL.split(' ')[0])}">
<style>
:root{{
  --bg-base:#0a0a0a; --bg-card:#141414; --bg-code:#0d0d0d;
  --orange:#ff6b35; --orange-bright:#ff8555; --orange-dim:rgba(255,107,53,.12); --orange-border:rgba(255,107,53,.4);
  --text-primary:#f5f5f5; --text-secondary:#a0a0a0; --text-mono:#d4d4d4; --text-dim:#6a6a6a;
  --def-bg:rgba(56,189,248,.08); --def-border:rgba(56,189,248,.4);
  --border:rgba(255,255,255,.08); --radius:12px; --radius-sm:8px;
  --sans:Inter,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
  --mono:"JetBrains Mono","SF Mono",Menlo,Consolas,monospace;
  --measure:72ch;
}}
*{{box-sizing:border-box}}
html{{scroll-behavior:smooth}}
@media (prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}}}
body{{margin:0;background:var(--bg-base);color:var(--text-primary);font-family:var(--sans);font-size:16px;line-height:1.65;-webkit-font-smoothing:antialiased}}
a{{color:var(--orange-bright);text-decoration:none;border-bottom:1px solid var(--orange-border)}}
a:hover,a:focus-visible{{border-bottom-color:var(--orange-bright)}}
:focus-visible{{outline:2px solid var(--orange);outline-offset:3px}}
.topbar{{display:flex;justify-content:space-between;align-items:center;gap:1rem;padding:14px 20px;border-bottom:1px solid var(--border);font-family:var(--mono);font-size:12px;letter-spacing:.06em;text-transform:uppercase}}
.topbar .brand{{color:var(--orange);white-space:nowrap}}
.topbar .ver{{white-space:nowrap}}
.topbar .brand a{{color:inherit;border:0}}
.topbar .ver{{color:var(--text-dim)}}
.wrap{{max-width:1080px;margin:0 auto;padding:0 20px}}
.hero{{padding:56px 0 24px;border-bottom:1px solid var(--border)}}
.eyebrow{{font-family:var(--mono);font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--text-dim);margin:0 0 14px}}
h1.title{{font-size:clamp(40px,7vw,72px);line-height:1;letter-spacing:-.03em;margin:0 0 6px;font-weight:700}}
h1.title span{{color:var(--orange)}}
.subtitle{{font-size:18px;color:var(--text-secondary);margin:0 0 34px}}
.thesis{{font-size:clamp(24px,3.4vw,38px);line-height:1.15;letter-spacing:-.02em;font-weight:600;max-width:24ch;margin:0 0 30px}}
.thesis em{{font-style:normal;color:var(--orange)}}
.seam{{display:block;width:100%;max-width:640px;height:auto;margin:6px 0 34px}}
.seam text{{font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase;fill:var(--text-dim)}}
.seam .gate-label{{fill:var(--orange)}}
dl.meta{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px 22px;margin:0 0 4px;padding:18px 20px;background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius)}}
.meta-item dt{{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--text-dim);margin:0 0 3px}}
.meta-item dd{{margin:0;font-size:14px;color:var(--text-mono);overflow-wrap:anywhere}}
.layout{{display:grid;grid-template-columns:230px minmax(0,1fr);gap:48px;padding:40px 0 64px}}
@media (max-width:860px){{.layout{{grid-template-columns:1fr;gap:24px}}}}
nav.toc{{position:sticky;top:20px;align-self:start;font-size:13px}}
@media (max-width:860px){{nav.toc{{position:static}}}}
nav.toc .toc-title{{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--text-dim);margin:0 0 10px}}
nav.toc ul{{list-style:none;margin:0;padding:0}}
nav.toc li{{margin:0;padding:6px 0;border-top:1px solid var(--border)}}
nav.toc li:last-child{{border-bottom:1px solid var(--border)}}
nav.toc a{{color:var(--text-secondary);border:0;display:block}}
nav.toc a:hover{{color:var(--text-primary)}}
nav.toc ul ul{{display:none}}
article{{max-width:var(--measure)}}
article h2{{font-size:26px;letter-spacing:-.02em;margin:48px 0 14px;padding-top:24px;border-top:1px solid var(--border);scroll-margin-top:24px}}
article h2:first-of-type{{border-top:0;padding-top:0;margin-top:0}}
article h3{{font-size:19px;margin:28px 0 8px}}
article p{{margin:0 0 14px;color:#e6e6e6}}
article p:has(> strong:first-child > code.id:first-child), article p:has(> strong:first-child){{}}
article strong{{color:var(--text-primary);font-weight:600}}
article em{{color:var(--text-secondary)}}
article ul,article ol{{padding-left:1.2rem;margin:0 0 14px}}
article li{{margin:0 0 6px;color:#e6e6e6}}
article code{{font-family:var(--mono);font-size:.86em;background:var(--bg-code);border:1px solid var(--border);border-radius:4px;padding:1px 6px;color:var(--text-mono)}}
article code.id{{color:var(--orange);border-color:var(--orange-border);background:var(--orange-dim);font-weight:500}}
article .kw{{font-family:var(--mono);font-size:.82em;letter-spacing:.04em;color:var(--text-primary);border-bottom:1px dotted var(--text-dim)}}
article table{{width:100%;border-collapse:collapse;font-size:14px;margin:12px 0 22px;display:block;overflow-x:auto}}
article th,article td{{text-align:left;vertical-align:top;padding:9px 12px;border-bottom:1px solid var(--border)}}
article th{{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--text-dim);font-weight:500}}
article hr{{border:0;border-top:1px solid var(--border);margin:32px 0}}
.def-block{{margin:0 0 8px;padding:20px 22px;background:var(--def-bg);border:1px solid var(--def-border);border-radius:var(--radius);color:var(--text-primary)}}
.def-block .tag{{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#7dd3fc;margin:0 0 8px}}
.def-block p{{margin:0;font-size:17px;line-height:1.55}}
footer{{border-top:1px solid var(--border);padding:28px 0 48px;color:var(--text-secondary);font-size:14px}}
footer .cite{{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius);padding:16px 18px;margin:0 0 18px;font-family:var(--mono);font-size:13px;color:var(--text-mono);overflow-wrap:anywhere}}
footer .cite .tag{{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--text-dim);margin:0 0 6px}}
footer .sig{{font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--text-dim);margin-top:24px}}
</style>
</head>
<body>
<div class="topbar"><div class="brand">■ <a href="https://b2tech.io">AISAC · B2 Tech</a></div><div class="ver">{esc(VERSION.split(" ")[0])} · {esc(STATUS.split(" ")[0])}</div></div>

<header class="hero"><div class="wrap">
  <p class="eyebrow">Workloop Spec · Request for Comments</p>
  <h1 class="title">Workloop <span>Spec</span></h1>
  <p class="subtitle">Especificação do Workloop Agêntico</p>
  <p class="thesis">Liberdade dentro do loop, <em>determinismo na costura</em>.</p>

  <svg class="seam" viewBox="0 0 640 150" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Dois loops agênticos ligados por uma costura com um gate determinístico no meio">
    <g fill="none" stroke="#a0a0a0" stroke-width="2">
      <path d="M150 75 a42 42 0 1 1 -12 -30"/>
      <path d="M534 75 a42 42 0 1 1 -12 -30"/>
    </g>
    <g fill="#a0a0a0">
      <path d="M138 45 l 8 -12 l 4 14 z"/>
      <path d="M522 45 l 8 -12 l 4 14 z"/>
    </g>
    <line x1="152" y1="75" x2="292" y2="75" stroke="#6a6a6a" stroke-width="2" stroke-dasharray="3 7" stroke-linecap="round"/>
    <line x1="348" y1="75" x2="488" y2="75" stroke="#6a6a6a" stroke-width="2" stroke-dasharray="3 7" stroke-linecap="round"/>
    <rect x="292" y="57" width="56" height="36" rx="6" fill="#0a0a0a" stroke="#ff6b35" stroke-width="2"/>
    <rect x="312" y="69" width="16" height="12" fill="#ff6b35"/>
    <text x="108" y="132" text-anchor="middle">loop</text>
    <text x="320" y="132" text-anchor="middle" class="gate-label">gate</text>
    <text x="492" y="132" text-anchor="middle">loop</text>
    <text x="222" y="62" text-anchor="middle">costura</text>
    <text x="418" y="62" text-anchor="middle">costura</text>
  </svg>

  <dl class="meta">{meta_html}</dl>
</div></header>

<div class="wrap layout">
  <nav class="toc" aria-label="Sumário"><p class="toc-title">Sumário</p>{toc_html}</nav>
  <article>
    <div class="def-block"><p class="tag">DEF-11 · Definição nuclear</p><p><strong>Workloop agêntico governado.</strong> Sistema de dois ou mais loops agênticos que interagem por canais explícitos (mensagem, evento ou estado compartilhado mediado), sob uma autoridade de política (a organização que os criou), em que nenhuma interação entre loops e nenhuma ação com efeito externo ocorre sem passar por gate determinístico que impõe as políticas e regras de negócio dessa autoridade.</p></div>
    <p style="margin:10px 0 36px;color:var(--text-dim);font-size:13px;font-family:var(--mono)">Texto normativo completo abaixo. Este é um rascunho para comentários: abra uma issue no repositório ou responda ao autor.</p>
    {body_html}
  </article>
</div>

<footer><div class="wrap">
  <div class="cite"><p class="tag">Como citar</p>Bracaioli, B. (2026). <em>Workloop Spec: Especificação do Workloop Agêntico</em> ({esc(VERSION.split(' ')[0])}). B2 Tech / protocolo AISAC. DOI: {esc(DOI)}. {esc(URL.split(' ')[0])}</div>
  <p>Texto sob <a href="https://creativecommons.org/licenses/by/4.0/deed.pt-br">CC BY 4.0</a>. "Workloop" e "workloop agêntico" são termos do protocolo AISAC; use livremente, com atribuição. Não há marca registrada sobre o termo.</p>
  <p class="sig">WORKLOOP SPEC · {esc(sig_version)} · BRUNO BRACAIOLI · B2 TECH · AISAC</p>
</div></footer>
</body>
</html>
"""

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(page, encoding="utf-8")
print(f"ok -> {OUT} ({len(page)} bytes) meta={list(meta.keys())}")
