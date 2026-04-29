#!/usr/bin/env python3
"""Serialise RDF source files (.rdf) to Turtle and JSON-LD.

Replaces serialise-vocabulary.sh + serialise-examples.sh.
Run from repo root: python src/scripts/serialise.py
"""

import json
from pathlib import Path

import rdflib

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def serialise(src: Path, out: Path) -> None:
    g = rdflib.Graph()
    g.parse(str(src))

    out.mkdir(parents=True, exist_ok=True)
    stem = src.stem

    ttl = g.serialize(format="turtle")
    ttl = ttl.replace("    ", "  ")
    (out / f"{stem}.ttl").write_text(ttl, encoding="utf-8")

    raw = g.serialize(format="json-ld")
    jsonld = json.dumps(json.loads(raw), indent=2, ensure_ascii=False)
    (out / f"{stem}.jsonld").write_text(jsonld, encoding="utf-8")

    print(f"  {src.name} -> {out.relative_to(REPO_ROOT) / stem}.(ttl|jsonld)")


def main() -> None:
    dist = REPO_ROOT / "dist"

    print("== Serialise RDF vocabulary ==")
    for f in sorted((REPO_ROOT / "src").glob("*.rdf")):
        serialise(f, dist)

    print("\n== Serialise RDF examples ==")
    for f in sorted((REPO_ROOT / "src" / "examples").glob("*.rdf")):
        serialise(f, dist / "examples")

    print("\nDone.")


if __name__ == "__main__":
    main()
