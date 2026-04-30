# mobilityDCAT-AP - Repository Structure POC

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
├── mobilitydcat-ap.rdf        # Ontology - primary source of truth (RDF/XML)
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
| `build-release.yml` | push to `release/*`, manual | `releases/X.Y.Z/` and `releases/latest/` if marked |
| `build-draft.yml` | push of `draft/*` tag, manual | `drafts/X.Y.Z-draft-A.B/` |
| `promote-latest.yml` | manual only | updates `LATEST_RELEASE` on `main` + copies already-built `releases/X.Y.Z/` to `releases/latest/` on `gh-pages` |

The build and deploy steps are split into two reusable workflows called by the above:

| Reusable workflow | Purpose |
|-------------------|---------|
| `reusable-build.yml` | Full build pipeline - serialise RDF, copy assets, build ReSpec spec, validate HTML, check references; uploads `dist/` as an artifact |
| `reusable-deploy-gh-pages.yml` | Pre-clean target directory on `gh-pages`, then deploy the artifact via plain `git` |

### Promoting a release to `releases/latest/`

`LATEST_RELEASE` in the repo root (on `main`) holds the version number currently marked as latest (e.g. `1.0.0`). On every push to a `release/*` branch, `build-release.yml` reads this file from `main` - if the version matches the branch, it also deploys to `releases/latest/` automatically.

This means:
- Hotfixes to the current latest release branch update `releases/latest/` automatically, just like they update the versioned directory.
- Hotfixes to older release branches only update their versioned directory - `releases/latest/` is untouched.

To promote a different version to latest:

- Run `promote-latest.yml` from the Actions tab and enter the version number.
- It updates `LATEST_RELEASE` on `main` (so future hotfixes to that branch also update `releases/latest/`).
- It also copies the already-built `releases/X.Y.Z/` to `releases/latest/` on `gh-pages` immediately - no rebuild needed.
- Promotion is an explicit, deliberate step - no version silently becomes latest without a human decision.

## Building locally

See `DEVELOPMENT.md` for prerequisites, setup, and build instructions.
