# Development guide

## Prerequisites

- [mise](https://mise.jdx.dev/) — manages Node.js and Python versions locally
- [Git for Windows](https://git-scm.com/download/win) (Windows only) — provides bash for any remaining shell scripts

## First-time setup

```sh
mise install          # installs Node 24 and Python 3.12 into the project
mise run install      # installs npm packages (respec) and pip packages (rdflib, pyshacl)
```

## Build

```sh
mise run build        # full build: serialise RDF + build ReSpec spec → dist/
```

Individual steps:

```sh
mise run serialise    # convert src/*.rdf and src/examples/*.rdf → .ttl + .jsonld
mise run build-spec   # copy assets to dist/ and build dist/index.html via ReSpec
```

## How it works

| Step | Script | What it does |
|------|--------|-------------|
| Serialise | `src/scripts/serialise.py` | Parses each `.rdf` with rdflib, writes sibling `.ttl` and `.jsonld` files |
| Copy assets | `src/scripts/copy-assets.py` | Copies ontology files, examples, figures, and SHACL shapes to `dist/` |
| Build spec | `src/scripts/build-spec.py` | Spins up a local HTTP server, runs `respec` against it, writes `dist/index.html` |

A local HTTP server is used for the ReSpec build step because Chromium (used by ReSpec internally) blocks `file://` requests needed by `data-include`.

## Source layout

All hand-authored files live under `src/`. Never edit files in `dist/` — they are generated.

| Path | Purpose |
|------|---------|
| `src/mobilitydcat-ap.rdf` | Ontology — primary source of truth (RDF/XML) |
| `src/index.html` | ReSpec specification document |
| `src/config.js` | ReSpec configuration (version, editors, dates) |
| `src/tables/` | HTML property tables included by `index.html` via `data-include` |
| `src/examples/` | Worked examples (RDF/XML, Turtle, JSON-LD) |
| `src/shaclShapes/` | SHACL validation constraints |
| `src/figures/` | UML diagrams |
| `src/scripts/` | Build scripts (Python) |

## Dependencies

| Tool | Version | Purpose |
|------|---------|---------|
| Node.js | 24 | Required by ReSpec |
| respec | 36.0.0 | Builds the HTML specification |
| Python | 3.12 | Required by build scripts |
| rdflib | 7.6.0 | RDF serialisation (`.rdf` → `.ttl`, `.jsonld`) |
| pyshacl | 0.31.0 | SHACL validation (optional, not run by default) |

Versions are pinned in `.mise.toml`, `package.json`, and `requirements.txt`.

## CI

The GitHub Actions workflow (`.github/workflows/build-main.yml`) mirrors the local build and publishes to `gh-pages` under `drafts/latest/` on every push to `main`.
