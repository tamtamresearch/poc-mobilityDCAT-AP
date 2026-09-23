# Response to NOTES.md

Date: 2026-09-23 (updated; first version 2026-09-21)
Repository state: `main` at `637d686`

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

## 3) Draft naming convention — DONE

Agreed and implemented:

| Ref | Kind | Publishes to |
|-----|------|--------------|
| `main` | branch | `drafts/latest/` |
| `draft/X.Y.Z-draft.N[.C]` | tag | `drafts/X.Y.Z-draft.N[.C]/` |
| `release/X.Y.Z` | branch | `releases/X.Y.Z/` |

`X.Y.Z` is the version the draft works towards, `N` is the review round,
counting from 1: `draft/3.0.0-draft.1`. The optional `C` is a correction
published inside the same round, `draft/3.0.0-draft.1.1`, for the case where a
snapshot has already been circulated and needs a fix that does not amount to a
new review round. The plain `draft.N` stays the normal form.

That optional second number is the only addition to the pattern as agreed; it
keeps the two-level form your `draft-0.1` example allowed. Dropping it again is
one character in one regular expression, if you would rather the form stayed at
a single number.

The reason for this shape rather than the previous `1.0.0-draft-0.1`:
`X.Y.Z-draft.N` is a valid SemVer pre-release, so ordering follows from the
SemVer rules instead of a local convention. Identifiers are compared left to
right, the numeric ones compare numerically rather than as text, and a longer
set of identifiers sorts above a shorter one when everything before it is equal:

```
3.0.0-draft.1  <  3.0.0-draft.1.1  <  3.0.0-draft.2  <  3.0.0-draft.10  <  3.0.0
```

`1.0.0-draft-0.1` gives none of that, because `draft-0` is a single alphanumeric
identifier and compares as text. The convention also matches how DCAT-AP labels
its own drafts by target version.

The rule is now enforced rather than described: `build-draft.yml` rejects
anything that is not `^[0-9]+\.[0-9]+\.[0-9]+(-draft\.[0-9]+(\.[0-9]+)?)?$` and
`build-release.yml` rejects anything that is not `^[0-9]+\.[0-9]+\.[0-9]+$`, so
a release branch cannot carry a pre-release suffix. Both guards were checked
against `3.0.0`, `3.0.0-draft.1`, `3.0.0-draft.1.0`, `3.0.0-draft.1.1`,
`3.0.0-draft.10` (accepted where intended) and `3.0`, `v3.0.0`, `3.0.0-draft`,
`3.0.0-draft-0.1`, `3.0.0-draft.1.2.3`, `main` (rejected).

The convention is stated once, in the README branching table. The workflow
header comments and the workflow `name:` lines were corrected to match; both
previously claimed a `vX.Y.Z` form that is not used anywhere.

## 4) Document the repository by procedures — DONE

New `PROCEDURES.md` at the repository root, the editor-facing "how do I do X"
document. `README.md` keeps describing the structure and the workflows,
`DEVELOPMENT.md` keeps being the setup and build guide, and both now link to it.

One section per procedure, each stating when it applies, the steps, and what
lands where on `gh-pages`:

1. Edit the current draft — branch, push, `build-check.yml` builds and publishes
   nothing, PR, merge, `build-main.yml` refreshes `drafts/latest/`.
2. Publish a named draft snapshot for review — set `config.js`, tag
   `draft/X.Y.Z-draft.N` on `main`, push the tag. Includes the point that the
   tag is permanent and the snapshot is never rebuilt, so a bad snapshot becomes
   `-draft.N+1` rather than a moved tag.
3. Create a release — set `config.js`, branch `release/X.Y.Z` from `main`, push.
   The `config.js` checklist sits inside this procedure as a step, not as a
   separate page.
4. Promote a release to latest — run `promote-latest.yml`, then confirm
   `LATEST_RELEASE` on `main` and the promote commit on `gh-pages`, which are
   two separate commits on two branches.
5. Hotfix a published release — commit on the existing `release/X.Y.Z` branch,
   bump the patch version, push; with the note that a hotfix to a non-latest
   branch leaves `releases/latest/` untouched, deliberately.

The document closes with a single table mapping every ref you can push to the
workflow it triggers and the directory it writes.

## 5) config.js checklist for drafts and releases — DONE

In `PROCEDURES.md`, inside procedure 3, as a table of field, line number, draft
value and release value: `publishDate`, `specStatus`, `latestVersion`,
`canonicalURI`, `prevRecURI`, `thisVersionURI`, `prevVersionURI`,
`latestVersionURI` and `edDraftURI`.

The checklist also covers two entries that are easy to miss because they are
hard-coded `otherLinks` rows rather than ReSpec fields: "Document version"
(`src/config.js:132-137`) and the "Previous version:" / "This version:" links
(`:140-145`), each of which carries the version number twice, in `value` and in
`href`. Those rows use the `mobilitydcat-ap.github.io` form of the URL while the
ReSpec fields above use `w3id.org`; both resolve, so the checklist asks for
internal consistency rather than unifying them.

The motivating observation is stated in the document itself: `main` today
carries `specStatus: "unofficial"` and `canonicalURI` pointing at
`drafts/latest/`, alongside `thisVersionURI` pointing at `releases/3.0.0/` and a
`publishDate` of `2026-10-01` — a mix of draft and release values.

On your sub-point about post-build HTML adjustment: the document says not to
edit the built HTML, because the next automated build overwrites `dist/`
entirely, and that anything not expressible in `config.js` belongs in
`src/index.html`.

**Question for the meeting.** Four of these fields are a pure function of the
ref that triggered the build and could be written into `config.js` by CI:
`thisVersionURI`, `canonicalURI`, `publishDate` and `specStatus`. Two cannot be:
`prevVersionURI` and `prevRecURI` need a human decision about which release is
superseded. Automating the first group removes four manual steps, at the cost of
a local build and a CI build producing different metadata from the same source.
Not implemented; worth ten minutes of discussion.

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

## 8) Agent instructions interoperability — DONE

Your instinct was right, with one correction: the emerging convention is
`AGENTS.md`, not `agent.md`, and several coding agents read it. Claude Code
reads `CLAUDE.md`, so `CLAUDE.md` is now a single line, `@AGENTS.md`, and the
content is vendor-neutral.

The more interesting part was what to put in it. The old `CLAUDE.md` was 87
lines that largely restated the README and `DEVELOPMENT.md`, and that
duplication is exactly what went stale: it still listed `validationFiles/` and
still described branch names we no longer use. Restating those documents in a
third place guarantees the same outcome again.

`AGENTS.md` therefore does not summarise them. It gives a table saying which of
the three documents answers which question, and adds only what lives nowhere
else:

- **`src/` is read-only in this repository**, with the reason: it mirrors
  upstream `drafts/latest`, and this repository exists to design a structure, so
  editing spec content here would make the two diverge. `src/scripts/` is the
  exception, being build tooling rather than content. An agent asked to fix one
  of the known defects should now say so and stop, rather than quietly editing
  `index.html`. This rule was applied throughout the work above but had not been
  written down anywhere.
- The `mise run lint` baseline: **1749 html-validate errors on an unmodified
  tree**, coming from ReSpec's generated markup rather than from the sources. An
  agent seeing that number cold reads it as 1749 defects to fix. It is a
  comparison baseline, and a change in it means something under `src/` moved.
- The LF rule from `.gitattributes` and why it exists, since a CRLF checkout
  silently changes the content of multi-line RDF literals.
- The commit subject prefixes this history uses (`CI:`, `Docs:`, `Dev:`).

The result is 83 lines that should not go stale, because nothing in it is a copy
of something maintained elsewhere.

## 9) Dev mode SHACL validation — AGREED AS FUTURE WORK

`pyshacl` is already a dependency and unused, so the groundwork is there. One
practical note for when it is picked up: `imports.ttl` pulls in external
vocabularies (DCAT, Dublin Core, FOAF, LOCN and others) and `mdr-imports.ttl`
adds 21 more `owl:imports`. A local task should be able to validate against
`shapes.ttl` and `ranges.ttl` without network access, with the full
import-based check as an option.

## Open actions

Points 3, 4, 5 and 8 are now done. What remains:

1. Fix the `enterpriseArchitectFiles` link: copy the folder into `dist/` or link
   to GitHub. **Needs your decision**, because it is a change to
   `src/index.html`; this repository treats the spec sources as read-only so
   they do not diverge from upstream `drafts/latest`.
2. Fix the stale 1.0.1 SHACL link in `index.html` to point at `releases/1.0.1/`.
   Same constraint as above.
3. Decide whether CI should fill in `thisVersionURI`, `canonicalURI`,
   `publishDate` and `specStatus` from the branch or tag name (see point 5).
4. Build the presentation from `PRESENTATION-BRIEFING.md` (point 6).
5. Drop or reconcile the colleague's timeout-fix branch against `d065a97`.
6. Later: add a mise task for SHACL validation, with an offline mode that skips
   the imports (point 9).

One observation for upstream, outside this repository: `src/shaclShapes/README.md:39`
still references `drafts/1.1.0-draft-0.1/shaclShapes` in the old naming. It was
left untouched here under the read-only rule.
