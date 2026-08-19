# Changelog

Todas as mudanças notáveis desta especificação são registradas aqui. O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e o versionamento segue [SemVer](https://semver.org/lang/pt-BR/): MAJOR para mudança incompatível em definições nucleares ou no invariante; MINOR para novos requisitos/corolários; PATCH para correções editoriais.

## [Unreleased]

## [0.1.0-rc3] - 2026-08-18

### Added
- DEF-13 (workloop composto: três costuras, contrato no nível do workloop, autoridade hierárquica) e DEF-14 (meta-loop).
- REQ-6 (meta-loop e auto-aprimoramento: só dentro do envelope; mudanças de política por costura humana; meta-loop não altera os gates que o governam).
- Parágrafo de posicionamento na seção 1 ("operada por IA, governada por humanos"); item "modelo define a própria política" na seção 9; composição e meta-loop no exemplo canônico; duas linhas novas no checklist.

### Changed
- DEF-10 admite componentes não agênticos; DEF-4 e DEF-9 cobrem a fronteira de workloop; COR-1 estende a atenuação à hierarquia; CONF-S exige gate nos três níveis e REQ-6; definições nucleares passam a DEF-10 a DEF-13.
- Requisitos operacionais deixam de ser marcados como propostos.

### Removed
- Seção 14 (questões em aberto): Q1 a Q4 incorporadas ao texto normativo.

## [0.1.0-rc2] - 2026-08-18

### Added
- Seção 14 com quatro questões em aberto levantadas na segunda leitura: componentes não agênticos (Q1), workloop composto e três níveis de costura (Q2), meta-loop e auto-aprimoramento dentro do envelope (Q3), posicionamento "operada por IA, governada por humanos" (Q4).

### Changed
- Remoção de travessões em todo o texto; URL canônica e repositório definidos.

## [0.1.0-rc1] - 2026-08-18

### Added
- Primeira versão pública para comentários.
- Definições DEF-1 a DEF-12 (loop agêntico, autoridade de política, canal, costura, gate determinístico, regra decidível, autoridade efetiva da cadeia, contrato de workloop, workloop agêntico, governado e aberto).
- Invariante INV-1 a INV-6 ("liberdade dentro do loop, determinismo na costura").
- Corolários COR-1 a COR-3 (atenuação de autoridade, rastreabilidade, canal implícito é defeito).
- Requisitos operacionais REQ-1 a REQ-5 (terminação, procedência, idempotência, contrato publicado, interrupção), propostos e abertos a comentário.
- Workloop aberto OPEN-1 a OPEN-5.
- Conformidade CONF-L, CONF-S, CONF-D e checklist (Apêndice A).
- Exemplo canônico, delimitação ("o que não é workloop") e relação com trabalhos anteriores.
