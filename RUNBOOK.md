# Runbook: do rascunho ao registro por publicação

Ordem recomendada. A maior parte é clique; o trabalho de verdade é o passo 0.

## 0. Revisar e reescrever (você)

- Leia `SPEC.md` inteiro e reescreva na sua voz o que quiser. Decida sobre REQ-1 a REQ-5 (estão marcados como propostos): manter, cortar ou mover.
- Decididos: hostname canônico `workloop.b2tech.io` e repositório `github.com/brunobracaioli/workloop-spec`.
- Depois de qualquer edição no `SPEC.md`, rode `python3 build.py` para regenerar `docs/index.html`.

## 1. Repositório público no GitHub

```bash
cd workloop-spec
git init -b main
git add .
git commit -m "Workloop Spec 0.1.0-rc3: rascunho para comentários"
git remote add origin https://github.com/brunobracaioli/workloop-spec.git   # repo criado vazio no site (sem README/.gitignore/licença)
git push -u origin main
git tag -a v0.1.0-rc3 -m "Workloop Spec 0.1.0-rc3"
git push --tags
```

- Ao criar o repositório no site: visibilidade Public, sem README, sem .gitignore, licença "No license" (o `LICENSE` com CC BY 4.0 já vem no pacote e o GitHub o detecta). Ative Issues (é o canal de comentários do RFC).
- Opcional: GitHub Pages em `main` `/docs` como espelho da página canônica.

## 2. DOI no Zenodo

**Rota A: DOI impresso no próprio texto do 0.1.0** (recomendada para a primeira versão):

1. zenodo.org → login (pode ser com a conta GitHub) → **New upload** → clique em **Reserve DOI**. O DOI é reservado antes de publicar.
2. Copie o DOI reservado para `SPEC.md` (tabela do topo e seção 12), `README.md`, `CITATION.cff` e `.zenodo.json`. Rode `build.py`, commit, crie o release `v0.1.0`.
3. No upload do Zenodo: anexe o zip do release (`SPEC.md`, `docs/index.html`, `LICENSE`, `CITATION.cff`, `CHANGELOG.md`); tipo *Publication → Technical note*; título, autor, licença CC BY 4.0, versão 0.1.0, idioma português. **Publish**. O DOI vira ativo.

**Rota B: integração GitHub** (para todas as versões seguintes):

1. zenodo.org → menu do usuário → **GitHub** → ligue o switch do repositório `workloop-spec`.
2. Cada *Release* no GitHub gera automaticamente uma versão no Zenodo com DOI próprio; o *concept DOI* agrupa todas. Os metadados vêm de `.zenodo.json` (já pronto).
3. Cole o badge do DOI (o Zenodo fornece o markdown) no `README.md`.

## 3. Página canônica no domínio (Cloudflare, via MCP)

- A página está no Worker `workloop-spec` com o domínio `workloop.b2tech.io` associado; republicar o HTML mantém a URL.
- Regra: a URL canônica não muda nunca. Versões antigas continuam acessíveis pelo release no GitHub e pelo DOI de versão no Zenodo.

## 4. Livro

- O capítulo sobre workloop cita: *Bracaioli, B. (2026). Workloop Spec: Especificação do Workloop Agêntico (v0.1.0). DOI + URL.*
- Quando o livro sair (ISBN + depósito legal), acrescente a referência ao livro na seção "Como citar" do spec (mudança PATCH).

## 5. Opcional: Biblioteca Nacional (EDA)

- Só depois de o texto estar reescrito na sua voz e congelado em 0.1.0.
- Site da Fundação Biblioteca Nacional → Escritório de Direitos Autorais → registro de obra intelectual (texto): preencha o requerimento, gere e pague a GRU (o valor vigente aparece no próprio sistema), envie o requerimento assinado e a cópia da obra conforme as instruções atuais do EDA, guarde o número do protocolo. A certidão vem depois.
- O que isso dá: data certa reconhecida no Brasil sobre o **texto**. Não protege a ideia nem o termo.

## 6. Divulgação

- Só depois de existir URL canônica e DOI: post no LinkedIn apontando para a URL, no formato RFC (pedido de comentários), depois carrossel no Instagram, depois aula e mentoria.
- Regra de nome: sempre "workloop agêntico" (o composto), nunca "Workloop" solto.

## 7. Ao mudar o texto

- Editorial → PATCH. Requisito novo → MINOR. Mudou definição nuclear ou invariante → MAJOR.
- Atualize `CHANGELOG.md`, crie tag e release (o Zenodo gera o DOI de versão), regenere e republique a página.
