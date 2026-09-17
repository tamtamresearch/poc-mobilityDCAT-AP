#!/usr/bin/env python3
"""Serialise Turtle source files (.ttl) to RDF/XML and JSON-LD.

Turtle is the source of truth. The RDF/XML and JSON-LD serialisations are
generated into dist/ on every build and are never committed.

Run from repo root: python src/scripts/serialise.py
"""

import json
from pathlib import Path

import rdflib

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def write(path: Path, text: str) -> None:
    """Write with LF endings, so Windows and CI produce identical files.

    Line breaks inside RDF literals are content: translating them to CRLF
    would change the data, not just the file.
    """
    path.write_text(text, encoding="utf-8", newline="\n")


def serialise(src: Path, out: Path) -> None:
    g = rdflib.Graph()
    g.parse(str(src))

    out.mkdir(parents=True, exist_ok=True)
    stem = src.stem

    rdf = g.serialize(format="pretty-xml")
    write(out / f"{stem}.rdf", rdf)

    raw = g.serialize(format="json-ld")
    jsonld = json.dumps(json.loads(raw), indent=2, ensure_ascii=False)
    write(out / f"{stem}.jsonld", jsonld)

    print(f"  {src.name} -> {out.relative_to(REPO_ROOT) / stem}.(rdf|jsonld)")


def main() -> None:
    dist = REPO_ROOT / "dist"

    print("== Serialise Turtle vocabulary ==")
    for f in sorted((REPO_ROOT / "src").glob("*.ttl")):
        serialise(f, dist)

    print("\n== Serialise Turtle examples ==")
    for f in sorted((REPO_ROOT / "src" / "examples").glob("*.ttl")):
        serialise(f, dist / "examples")

    print("\nSerialise Done.")


if __name__ == "__main__":
    main()
