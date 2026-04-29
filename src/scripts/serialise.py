#!/usr/bin/env python3
"""Serialise RDF source files (.rdf) to Turtle and JSON-LD.

Replaces serialise-vocabulary.sh + serialise-examples.sh.
Run from repo root: python src/scripts/serialise.py
"""

import json
from pathlib import Path

import rdflib

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def serialise(src: Path) -> None:
    g = rdflib.Graph()
    g.parse(str(src))

    stem = src.stem
    out = src.parent

    ttl = g.serialize(format="turtle")
    ttl = ttl.replace("    ", "  ")
    (out / f"{stem}.ttl").write_text(ttl, encoding="utf-8")

    raw = g.serialize(format="json-ld")
    jsonld = json.dumps(json.loads(raw), indent=2, ensure_ascii=False)
    (out / f"{stem}.jsonld").write_text(jsonld, encoding="utf-8")

    print(f"  {src.name} -> .ttl + .jsonld")


def main() -> None:
    print("== Serialise RDF vocabulary ==")
    for f in sorted((REPO_ROOT / "src").glob("*.rdf")):
        serialise(f)

    print("\n== Serialise RDF examples ==")
    for f in sorted((REPO_ROOT / "src" / "examples").glob("*.rdf")):
        serialise(f)

    print("\nDone.")


if __name__ == "__main__":
    main()
