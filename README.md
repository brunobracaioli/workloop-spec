# Workloop Spec

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22004648.svg)](https://doi.org/10.5281/zenodo.22004648)

**Agentic Workloop Specification** · version 0.1.0-rc5 (draft for review) · AISAC protocol · B2 Tech

> Probabilistic autonomy for thinking. Deterministic governance for acting.
>
> Invariant: freedom inside the loop, a deterministic gate at every interface.

An **agentic workloop** is a system of two or more agentic loops that interact through explicit channels. When all participants are under one policy authority (the organization that created them), the workloop is **governed**: no inter-loop interaction and no externally effecting action may occur without passing through a deterministic gate that enforces that authority's policies and business rules. When the graph crosses the authority boundary, the workloop is **open** and defensive rules apply.

The Portuguese translation remains available as a secondary language in [`README.pt-BR.md`](README.pt-BR.md) and [`SPEC.md`](SPEC.md).

| | |
|---|---|
| Normative text | [`SPEC.en.md`](SPEC.en.md) |
| Portuguese text | [`SPEC.md`](SPEC.md) |
| Canonical page | https://workloop.b2tech.io  |
| DOI | [10.5281/zenodo.22004648](https://doi.org/10.5281/zenodo.22004648) |
| License | [CC BY 4.0](LICENSE) |
| Changes | [`CHANGELOG.md`](CHANGELOG.md) |
| How to cite | [`CITATION.cff`](CITATION.cff) |

## Status

Draft for comments (*Request for Comments*). Open an issue to propose changes to definitions, the invariant, corollaries, or requirements. At `0.1.0`, the text freezes and follows SemVer (see section 13 of the spec).

## Name

"Workloop" and "agentic workloop" are terms of the AISAC protocol (Bruno Bracaioli / B2 Tech). Use them freely with attribution to this specification. The term is not trademarked.

## How to cite

Bracaioli, B. (2026). *Workloop Spec: Agentic Workloop Specification* (version 0.1.0). B2 Tech / AISAC protocol. DOI: 10.5281/zenodo.22004648. https://workloop.b2tech.io

## Licenses

Specification text: CC BY 4.0 (`LICENSE`). Script `build.py`: MIT (SPDX header).

## Build the pages

```bash
pip install markdown
python3 build.py   # writes docs/index.html (EN) and docs/pt-br.html (pt-BR)
```

`SPEC.en.md` is the default English source. `SPEC.md` remains the source for the Portuguese translation. Both pages are generated from their respective sources.
