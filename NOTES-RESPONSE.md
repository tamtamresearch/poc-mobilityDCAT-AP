# Response to NOTES.md

Date: 2026-09-21
Repository state: `main` at `b3cf319`

This answers each point in `NOTES.md` (dated 2026-09-16) and records what has
been done since. Several notes were already overtaken by the sync commit
`a64b0ba`, which brought `src/` in line with the current `drafts/latest` of the
upstream repository.

## 1) Serialization direction change on main — DONE

Turtle is now the source format for both the ontology and the examples
(commit `b3cf319`).

- `src/mobilitydcat-ap.ttl` is the ontology source. It was converted from the
  previous `.rdf` source with rdflib, so all 1534 triples are carried over.
  `src/mobilitydcat-ap.rdf` is gone.
- The examples keep only their `.ttl` files. The committed `.rdf` and `.jsonld`
  copies were verified to contain the same triples, then deleted.
- `serialise.py` reads `src/*.ttl` and `src/examples/*.ttl` and writes `.rdf`
  (pretty-xml) and `.jsonld` into `dist/`. `copy-assets.py` copies the Turtle
  sources.
- README, `CLAUDE.md` and `DEVELOPMENT.md` describe Turtle as the source of
  truth.

Two details worth knowing, because both silently change the data:

- The old script compacted indentation with `ttl.replace("    ", "  ")`. That
  also rewrites four spaces occurring inside multi-line `rdfs:comment`
  literals. Harmless in a throwaway `dist/` file, damaging in a committed
  source, so it was dropped.
- Writing text on Windows turns `\n` into `\r\n`, including inside literals.
  `serialise.py` now writes with `newline="\n"`, and a new `.gitattributes`
  forces `eol=lf` for `.ttl`, `.rdf` and `.jsonld`. Without it, `core.autocrlf`
  would check the Turtle source out with CRLF and a local build would produce
  different literals than CI.

Also fixed in passing: `mise run build` used to list `serialise` and
`build-spec` as parallel dependencies, so which files ended up in `dist/`
depended on which step finished last. `build-spec` now depends on `serialise`.

Verification: the build takes about 6 s, every generated file is isomorphic to
the file it replaced, `check-refs.py` reports no broken local references, and
html-validate reports 1749 errors, the same count as before the change.

## 2) Reflect the new drafts/latest structure — MOSTLY DONE

Done by the sync commit `a64b0ba`:

- `validationFiles/` is gone from `src/`. Its last stale mentions in the README
  tree and the `CLAUDE.md` layout table were removed in `b3cf319`.
- Examples replaced with `example-minimum` and `example-complete`.
- `shaclShapes/` replaced with `shapes.ttl`, `ranges.ttl`, `mdr-vocabularies.ttl`,
  `imports.ttl`, `mdr-imports.ttl` and `deprecated-uris.ttl`, plus a README.
- Other changes the note did not list: new figures (`Fig1`–`Fig4`), new tables
  `dcat-ap-not-used-properties.html` and `properties-deprecated.html`, and a
  `config.js` that offers the SHACL files as alternate formats. The old
  `scripts/*.sh`, `scripts/*.php` and `catalog-v001.xml` were deliberately left
  out.

One correction: `enterpriseArchitectFiles/` **is** still part of the upstream
`drafts/latest` and is still in `src/`. What is broken is the link to it.
`src/index.html:1123` links to `./enterpriseArchitectFiles`, but
`copy-assets.py` does not copy that folder into `dist/`, so the link is dead on
the published page. Either copy the folder or point the link at GitHub.

Still open: the change-log entry for release 1.0.1 (`src/index.html:1413`)
links to `./shaclShapes/mobilitydcat-ap_shacl_shapes.ttl`, which no longer
exists under `drafts/latest`. The file it means is published at
`https://mobilitydcat-ap.github.io/mobilityDCAT-AP/releases/1.0.1/mobilitydcat-ap_shacl_shapes.ttl`
(the `w3id.org` form of that address returns 404).

## 3) Draft naming convention — OPEN

The convention exists, but only as an example: README and the comment in
`build-draft.yml` both use `draft/1.0.0-draft-0.1`, publishing to
`drafts/1.0.0-draft-0.1/`. The guard in `build-draft.yml` only tests
`^[0-9]+\.[0-9]+`, so a tag such as `draft/1.0-anything` passes. Once the
pattern is agreed, tighten that regular expression to match it, so the rule is
enforced and not merely documented.

`CLAUDE.md` still describes an older convention (`release/vX.Y`,
`draft/topic-name`) and points to the deleted `PLAN.md`.

## 4) Document the repository by procedures — OPEN

Agreed. The README is organised around the workflow files, which suits
maintainers but not editors. The release sequence in the note is correct, but a
step is missing: `config.js` has to be set for the release before the branch is
pushed (see point 5). Worth adding as well: a hotfix to an already published
release, and tagging a draft snapshot for review.

## 5) config.js checklist for drafts and releases — OPEN

Needed, and the current file shows why: on `main` (the draft) it carries
`specStatus: "unofficial"` and a `canonicalURI` pointing at `drafts/latest`, but
also `thisVersionURI: .../releases/3.0.0/` and `publishDate: "2026-10-01"`.

The checklist should cover at least `specStatus`, `publishDate`,
`thisVersionURI`, `prevVersionURI`, `prevRecURI`, `canonicalURI`,
`latestVersion` and `edDraftURI`.

Some of these could be filled in by the workflow from the branch or tag name,
which would shorten the manual checklist. Editing the built HTML afterwards
should be avoided, because the next automated build overwrites it; anything
that cannot be expressed in `config.js` belongs in `index.html`.

## 6) Presentation of refactoring objectives — OPEN

Nothing technical to add. `PRESENTATION-BRIEFING.md` already contains a
"what is painful today" table that covers the three goals and can serve as the
outline.

## 7) ReSpec CI timeout — DONE

Fixed on `main` in `d065a97`. `build-spec.py` now runs
`respec --localhost --use-local --timeout 120`. The error quoted in the note
("Navigation timeout ... 620 ms") has the same cause as the one seen in CI:
ReSpec's default limit of 10 s covers the whole run, browser launch included.

The `npx respec` fallback was not added and does not appear to be needed: CI
puts `node_modules/.bin` on `PATH` (`reusable-build.yml:48`), and mise does the
same locally.

Action: the separate branch carrying the other version of this fix should be
dropped or compared against `d065a97`, so the two do not conflict.

## 8) Agent instructions interoperability — OPEN

The emerging convention is `AGENTS.md`, not `agent.md`; several coding agents
read it. Claude Code reads `CLAUDE.md`, so the usual arrangement is a one-line
`CLAUDE.md` that imports `@AGENTS.md`.

There is a second reason to do this: `CLAUDE.md` largely duplicates the README
and `DEVELOPMENT.md`, and duplication is what went stale (`PLAN.md`,
`validationFiles/`, the old branch names). A short `AGENTS.md` that points at
the README and `DEVELOPMENT.md` and adds only agent-specific rules would stay
accurate by itself.

## 9) Dev mode SHACL validation — AGREED AS FUTURE WORK

`pyshacl` is already a dependency and unused, so the groundwork is there. One
practical note for when it is picked up: `imports.ttl` pulls in external
vocabularies (DCAT, Dublin Core, FOAF, LOCN and others) and `mdr-imports.ttl`
adds 21 more `owl:imports`. A local task should be able to validate against
`shapes.ttl` and `ranges.ttl` without network access, with the full
import-based check as an option.

## Open actions

1. Fix the `enterpriseArchitectFiles` link: copy the folder into `dist/` or link
   to GitHub.
2. Fix the stale 1.0.1 SHACL link in `index.html` to point at `releases/1.0.1/`.
3. Agree the draft tag pattern, state it once in the README, and tighten the
   regular expression in `build-draft.yml`.
4. Write procedure-based documentation: edit the draft, tag a draft, create a
   release, promote to latest, hotfix a release.
5. Write the `config.js` checklist for drafts and releases, and decide which
   fields CI can fill in.
6. Build the presentation from `PRESENTATION-BRIEFING.md`.
7. Drop or reconcile the colleague's timeout-fix branch against `d065a97`.
8. Replace `CLAUDE.md` with a short `AGENTS.md` plus a `CLAUDE.md` that imports
   it, and remove the remaining `PLAN.md` reference.
9. Later: add a mise task for SHACL validation, with an offline mode that skips
   the imports.
10. `release/4.0.0` (local and on origin) sits at `17f77b1`, which predates the
    ReSpec timeout fix, `build-check.yml` and the sync. Any push to it will
    build without the fix. Bring it up to date with `main` or delete it.
