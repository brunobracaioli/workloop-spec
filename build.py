#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Gera as páginas da especificação em inglês e português.

Uso: python3 build.py
Requer: pip install markdown
"""
import re
import html as htmlmod
from pathlib import Path

import markdown

ROOT = Path(__file__).parent
LANGUAGES = {
    "en": {
        "source": ROOT / "SPEC.en.md",
        "output": ROOT / "docs" / "index.html",
        "html_lang": "en",
        "labels": {"Version", "Status", "Date", "Author", "Canonical URL", "DOI", "License", "Repository"},
        "title": "Agentic Workloop Specification",
        "canonical": "https://workloop.b2tech.io",
        "description": "Workloop Spec: a specification for agentic loops interacting under one policy authority, with a deterministic gate at every interface. AISAC protocol · B2 Tech.",
        "og_description": "Probabilistic autonomy for thinking. Deterministic governance for acting. Terms, invariant, corollaries, and conformance for agentic workloops.",
        "subtitle": "Agentic Workloop Specification",
        "thesis": ("Probabilistic autonomy for thinking.", "Deterministic governance for acting."),
        "invariant_label": "Technical invariant",
        "invariant": "Freedom inside the loop. <b>A deterministic gate at every interface.</b>",
        "definition": "Governed agentic workloop",
        "definition_tag": "Core definition",
        "definition_text": "A system of two or more agentic loops that interact through explicit channels (message, event, or mediated shared state), under one policy authority (the organization that created them), in which no inter-loop interaction and no action with external effect occurs without passing through a deterministic gate that enforces that authority's policies and business rules.",
        "normative_note": "Full normative text below. This is a draft for comments: open an issue in the repository or reply to the author.",
        "toc": "Table of contents",
        "citation_label": "How to cite",
        "citation_title": "Workloop Spec: Agentic Workloop Specification",
        "license_text": "Text licensed under",
        "terms_text": '"Workloop" and "agentic workloop" are terms of the AISAC protocol; use them freely with attribution. The term is not trademarked.',
        "switch": '<a href="pt-br.html" hreflang="pt-BR">Português (Brasil)</a>',
        "alternate": "Portuguese (Brazil)",
    },
    "pt-BR": {
        "source": ROOT / "SPEC.md",
        "output": ROOT / "docs" / "pt-br.html",
        "html_lang": "pt-BR",
        "labels": {"Versão", "Status", "Data", "Autor", "URL canônica", "DOI", "Licença", "Repositório"},
        "title": "Especificação do Workloop Agêntico",
        "canonical": "https://workloop.b2tech.io/pt-br.html",
        "description": "Workloop Spec: especificação do workloop agêntico, sistema de loops agênticos que interagem sob uma autoridade de política, com gate determinístico em toda interface. Protocolo AISAC · B2 Tech.",
        "og_description": "Autonomia probabilística para pensar. Governança determinística para agir. Termos, invariante, corolários e conformidade do workloop agêntico.",
        "subtitle": "Especificação do Workloop Agêntico",
        "thesis": ("Autonomia probabilística para pensar.", "Governança determinística para agir."),
        "invariant_label": "Invariante técnico",
        "invariant": "Liberdade dentro do loop. <b>Gate determinístico em toda interface.</b>",
        "definition": "Workloop agêntico governado",
        "definition_tag": "Definição nuclear",
        "definition_text": "Sistema de dois ou mais loops agênticos que interagem por canais explícitos (mensagem, evento ou estado compartilhado mediado), sob uma autoridade de política (a organização que os criou), em que nenhuma interação entre loops e nenhuma ação com efeito externo ocorre sem passar por gate determinístico que impõe as políticas e regras de negócio dessa autoridade.",
        "normative_note": "Texto normativo completo abaixo. Este é um rascunho para comentários: abra uma issue no repositório ou responda ao autor.",
        "toc": "Sumário",
        "citation_label": "Como citar",
        "citation_title": "Workloop Spec: Especificação do Workloop Agêntico",
        "license_text": "Texto sob",
        "terms_text": '"Workloop" e "workloop agêntico" são termos do protocolo AISAC; use livremente, com atribuição. Não há marca registrada sobre o termo.',
        "switch": '<a href="index.html" hreflang="en">English</a>',
        "alternate": "English",
    },
}

def esc(x: str) -> str:
    return htmlmod.escape(x, quote=True)

def linkify(v: str) -> str:
    m = re.search(r"https?://\S+", v)
    if not m:
        return esc(v)
    u = m.group(0)
    return esc(v).replace(esc(u), f'<a href="{esc(u)}">{esc(u)}</a>')

def build_page(language: dict) -> tuple[Path, int]:
    text = language["source"].read_text(encoding="utf-8")

    # --- 1. Extract metadata table immediately after the subtitle ---------
    meta = {}
    lines = text.splitlines()
    body_lines = []
    in_meta = False
    labels = language["labels"]
    for ln in lines:
        if ln.startswith("| ") and "|---" not in ln and not in_meta:
            match = re.match(r"^\| (.+?) \|", ln)
            if match and match.group(1).strip() in labels:
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
    body_md = re.sub(r"^\| \| \|\n\|---\|---\|\n", "", body_md, flags=re.M)
    body_md = re.sub(r"^# Workloop Spec\n\n\*\*.*?\*\*\n\n", "", body_md, count=1)

    # --- 2. Markdown -> HTML -----------------------------------------------
    md = markdown.Markdown(extensions=["tables", "toc", "attr_list", "sane_lists"], extension_configs={"toc": {"toc_depth": "2"}})
    body_html = md.convert(body_md)
    toc_html = md.toc

    # --- 3. Highlight identifiers and normative keywords -------------------
    id_re = re.compile(r"(?<![\w-])((?:DEF|INV|COR|REQ|OPEN|CONF)-(?:\d+|[LSD]))(?![\w-])")
    kw_re = re.compile(r"(?<![\wÀ-ÿ])(MUST NOT|MUST|SHOULD NOT|SHOULD|MAY|NÃO DEVERIA|NÃO DEVEM|NÃO DEVE|DEVERIA|DEVEM|DEVE|PODEM|PODE)(?![\wÀ-ÿ])")

    def decorate(seg: str) -> str:
        return kw_re.sub(r'<span class="kw">\1</span>', id_re.sub(r'<code class="id">\1</code>', seg))

    parts = re.split(r"(<code>.*?</code>|<pre>.*?</pre>|<h[1-6][^>]*>.*?</h[1-6]>|<[^>]+>)", body_html, flags=re.S)
    body_html = "".join(part if part.startswith("<") else decorate(part) for part in parts if part)

    # --- 4. Fill the shared template ---------------------------------------
    version = meta.get("Version", meta.get("Versão", ""))
    status = meta.get("Status", "")
    date = meta.get("Date", meta.get("Data", ""))
    author = meta.get("Author", meta.get("Autor", ""))
    url = meta.get("Canonical URL", meta.get("URL canônica", ""))
    doi = meta.get("DOI", "")
    license_name = meta.get("License", meta.get("Licença", ""))
    repo = meta.get("Repository", meta.get("Repositório", ""))
    meta_items = [("Version", version), ("Status", status), ("Date", date), ("Author", author),
                  ("License", license_name), ("DOI", doi), ("Canonical URL", url), ("Repository", repo)]
    meta_html = "".join(f'<div class="meta-item"><dt>{esc(k)}</dt><dd>{linkify(v)}</dd></div>' for k, v in meta_items if v)
    sig_version = version.split(" ")[0].upper()
    citation = (f'Bracaioli, B. (2026). <em>{esc(language["citation_title"])}</em> ({esc(version.split(" ")[0])}). '
                f'B2 Tech / AISAC protocol. DOI: <a href="https://doi.org/10.5281/zenodo.22004648">10.5281/zenodo.22004648</a>. '
                "https://workloop.b2tech.io")
    template = (ROOT / "template.html").read_text(encoding="utf-8")
    replacements = {
        "{{LANG}}": language["html_lang"], "{{PAGE_TITLE}}": language["title"],
        "{{CANONICAL_URL}}": language["canonical"],
        "{{DESCRIPTION}}": language["description"], "{{OG_DESCRIPTION}}": language["og_description"],
        "{{SUBTITLE}}": language["subtitle"], "{{THESIS_A}}": language["thesis"][0],
        "{{THESIS_B}}": language["thesis"][1], "{{INVARIANT_LABEL}}": language["invariant_label"],
        "{{INVARIANT}}": language["invariant"], "{{DEFINITION_LABEL}}": language["definition"],
        "{{DEFINITION_TAG}}": language["definition_tag"],
        "{{DEFINITION_TEXT}}": language["definition_text"], "{{NORMATIVE_NOTE}}": language["normative_note"],
        "{{TOC_LABEL}}": language["toc"], "{{CITATION_LABEL}}": language["citation_label"],
        "{{CITATION}}": citation, "{{LICENSE_TEXT}}": language["license_text"],
        "{{TERMS_TEXT}}": language["terms_text"], "{{LANG_SWITCH}}": language["switch"],
        "{{ALTERNATE_LANGUAGE}}": language["alternate"], "{{META_DL}}": meta_html,
        "{{TOC}}": '<div class="toc">\n' + toc_html.split('<div class="toc">', 1)[1] if '<div class="toc">' in toc_html else toc_html,
        "{{BODY}}": body_html, "{{VER_SHORT}}": sig_version.lower(), "{{VER}}": version.split(" ")[0],
        "{{VER_UPPER}}": sig_version,
    }
    page = template
    for key, value in replacements.items():
        page = page.replace(key, value)
    output = language["output"]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(page, encoding="utf-8")
    return output, len(page)

for language in LANGUAGES.values():
    output, size = build_page(language)
    print(f"ok -> {output} ({size} bytes)")
