# mobilityDCAT-AP — Repository Structure POC

> **This is a proof of concept** demonstrating a proposed repository layout and GitHub Actions publishing workflow for mobilityDCAT-AP. It is not the authoritative specification repository.
>
> The goal is to validate the branch-based versioning strategy (see `PLAN.md`) before applying it to the main repo.

## Source files

All hand-authored source files live in `src/`. Generated artefacts go in `dist/` and must not be edited by hand.

## Structure

```
src/
├── appendices/                          # Appendix content (placeholder)
├── config.js                            # ReSpec configuration (version, editors, dates)
├── index.html                           # ReSpec specification document (entry point)
├── mobilitydcat-ap.rdf                  # Ontology — primary source of truth (RDF/XML)
├── enterpriseArchitectFiles/            # Enterprise Architect model files
│   ├── mobilityDCAT-AP.qea              # EA project file
│   └── readme.md
├── examples/                            # Worked examples
│   ├── README.md
│   ├── *.ttl                            # Turtle examples
│   ├── *.jsonld                         # JSON-LD examples
│   └── SE NAP_dataset_*/               # Swedish NAP reference examples (.ttl, .xml)
├── figures/                             # UML diagrams and visual assets
│   └── mobilityDCAT-AP_uml-diagramm_*.png
├── js/
│   └── script.js                        # Custom JavaScript
├── scripts/                             # Build tooling
│   ├── run-all.sh                       # Top-level entry point
│   ├── build-all.sh                     # Builds all HTML tables
│   ├── build-class-tables.php           # Generates class/property tables from ontology
│   ├── build-summary-tables.php         # Generates summary tables
│   ├── build-example-index.php          # Indexes examples
│   ├── serialise-all.sh                 # Runs all serialisation steps
│   ├── serialise-vocabulary.sh          # Converts ontology to .ttl and .jsonld
│   └── serialise-examples.sh            # Serialises example files
├── shaclShapes/                         # SHACL validation constraints
│   ├── mobilitydcat-ap_shacl_shapes.ttl
│   └── readme.md
└── tables/                              # HTML property tables (included by index.html)
    ├── class-*.html                     # Per-class property tables
    ├── mandatory/recommended/optional-properties-for-*.html
    └── (+ summary, mapping, vocabulary tables)
```

## Branching convention

| Branch | Contents |
|--------|----------|
| `main` | Latest draft in progress |
| `release/vX.Y` | Frozen approved version |
| `draft/topic-name` | Parallel topic work, PR'd into `main` |

## Building

```bash
cd src/scripts
./run-all.sh
```

Output lands in `dist/` at the repository root.
