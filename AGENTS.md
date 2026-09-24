# Agent instructions

Guidance for coding agents working in this repository. Vendor-neutral by
design: `CLAUDE.md` imports this file rather than restating it.

## What this project is

**mobilityDCAT-AP** is a European standard, an RDF/OWL application profile of
DCAT-AP for describing mobility datasets, data services and services across
National Access Points in Europe. It is maintained by
[NAPCORE](https://napcore.eu/).

**This repository is a proof of concept**, not the authoritative specification
repository. It exists to validate a proposed layout and publishing workflow
before that structure is applied to the upstream repository at
https://github.com/mobilityDCAT-AP/mobilityDCAT-AP.

## Where the documentation is

This file deliberately does not repeat what the three documents below say. Read
the relevant one instead of relying on a summary here; a summary is what went
stale last time.

| Question | Document |
|----------|----------|
| What is in the repository, which workflow publishes where, the branch and tag naming convention | `README.md` |
| How to install the toolchain, build, lint, preview | `DEVELOPMENT.md` |
| How to edit the draft, publish a snapshot, cut a release, promote it, hotfix it, and what to set in `config.js` | `PROCEDURES.md` |

## Hard rules

**Treat `src/` as read-only.** `src/index.html`, `src/config.js`, `src/*.ttl`,
`src/tables/`, `src/figures/`, `src/shaclShapes/` and `src/examples/` are a
mirror of the upstream `drafts/latest`. This repository designs a structure that
is later applied upstream, so editing the specification content here would make
the two diverge and invalidate the comparison. Changes to spec content belong
upstream.

The exception is `src/scripts/`, which is build tooling rather than
specification content and is owned by this repository.

If a task appears to require a spec-content change, say so and stop rather than
making it. Several known defects are deliberately left in place for this reason;
they are recorded as open actions in `NOTES-RESPONSE.md`.

**Never edit `dist/`.** It is deleted and regenerated on every build. A fix
applied there survives until the next build and no longer.

**Never commit generated RDF.** Turtle is the source format for the ontology and
the examples. The `.rdf` and `.jsonld` serialisations are produced by
`serialise.py` into `dist/` on every build.

## Verifying a change

```sh
mise run lint      # full build + HTML validation + broken reference check + SHACL validation
```

Three things to know about the output, so they are not mistaken for regressions
introduced by the change at hand:

- `html-validate` reports **1749 errors** on an unmodified tree. They come from
  the ReSpec-generated markup, not from the sources. The number is a baseline to
  compare against, not a defect list to work through. If it moves, something in
  `src/` was touched.
- `check-refs.py` should report **no broken local references**. ReSpec prints
  only a count; this script prints the actual list.
- `validate-examples.py` should report **no violations**, with 4 warnings on
  `example-minimum.ttl` and 6 on `example-complete.ttl`. The warnings are known
  and recorded in `NOTES-RESPONSE.md` point 9. Its first run downloads the
  SHACL imports, and a failed download of the schema.org import is expected.

## Conventions

- Commit subjects carry a prefix matching the history: `CI:` for workflow
  changes, `Docs:` for documentation, `Dev:` for tooling and build scripts.
- Text files use LF endings. `.gitattributes` forces `eol=lf` for `.ttl`, `.rdf`
  and `.jsonld`, because a CRLF checkout on Windows changes the content of
  multi-line RDF literals and makes a local build differ from CI.
- Build scripts are Python and must run unchanged on Windows and Linux. No bash.

## External links

- Published spec: https://w3id.org/mobilitydcat-ap/releases/
- Latest draft: https://w3id.org/mobilitydcat-ap/drafts/latest/
- Upstream issues: https://github.com/mobilityDCAT-AP/mobilityDCAT-AP/issues
- Namespace: `http://w3id.org/mobilitydcat-ap#`
