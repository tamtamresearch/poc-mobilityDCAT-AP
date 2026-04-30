# mobilityDCAT-AP — Repository Structure POC

> **This is a proof of concept** demonstrating a proposed repository layout and GitHub Actions publishing workflow for mobilityDCAT-AP. It is not the authoritative specification repository.
>
> The goal is to validate the branch-based versioning strategy (see `PLAN.md`) before applying it to the main repo.

## Source files

All hand-authored source files live in `src/`. Generated artefacts go in `dist/` and must not be edited by hand.

## Structure

```
src/
├── index.html                 # ReSpec specification document (entry point)
├── config.js                  # ReSpec configuration
├── mobilitydcat-ap.rdf        # Ontology — primary source of truth (RDF/XML)
├── tables/                    # HTML property tables included by index.html
├── examples/                  # Worked examples
├── figures/                   # UML diagrams and logo
├── shaclShapes/               # SHACL validation constraints
├── validationFiles/           # Granular SHACL shapes (one per class)
├── js/                        # Custom JavaScript
├── scripts/                   # Build scripts (Python); see DEVELOPMENT.md
├── enterpriseArchitectFiles/  # EA model (.qea)
└── appendices/                # Appendix content (placeholder)
```

## Branching convention

| Ref | Type | Published to |
|-----|------|-------------|
| `main` | Latest draft | `drafts/latest/` |
| `release/1.0.0` | Release branch | `releases/1.0.0/` |
| `draft/1.0.0-draft-0.1` | Draft tag | `drafts/1.0.0-draft-0.1/` |

## GitHub Actions workflows

Workflows live in `.github/workflows/` and publish to the `gh-pages` branch.

| Workflow | Trigger | Publishes to |
|----------|---------|-------------|
| `build-main.yml` | push to `main` (src changes), manual | `drafts/latest/` |
| `build-release.yml` | push to `release/*`, manual | `releases/X.Y.Z/` |
| `build-draft.yml` | push of `draft/*` tag, manual | `drafts/X.Y.Z-draft-A.B/` |
| `promote-latest.yml` | manual only | `releases/latest/` ← copy of chosen version |

The build and deploy steps are split into two reusable workflows called by the above:

| Reusable workflow | Purpose |
|-------------------|---------|
| `reusable-build.yml` | Full build pipeline — serialise RDF, copy assets, build ReSpec spec, validate HTML, check references; uploads `dist/` as an artifact |
| `reusable-deploy-gh-pages.yml` | Pre-clean target directory on `gh-pages`, then deploy the artifact |

`releases/latest/` is **never updated automatically**. After verifying a release, run `promote-latest.yml` from the Actions tab and enter the version number (e.g. `1.0.0`). This makes promotion an explicit, deliberate step — pushing a fix to an older release branch will not silently overwrite latest.

## Building locally

```bash
mise run build
```

Output lands in `dist/` at the repository root. See `DEVELOPMENT.md` for prerequisites and setup.
