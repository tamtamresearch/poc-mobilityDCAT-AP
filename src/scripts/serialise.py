#!/usr/bin/env python3
"""Serialise Turtle source files (.ttl) to RDF/XML and JSON-LD.

Turtle is the source of truth. The RDF/XML and JSON-LD serialisations are
generated into dist/ on every build and are never committed.

Run from repo root: python src/scripts/serialise.py
"""

import json
import warnings
from io import BytesIO
from pathlib import Path

import rdflib
from rdflib import RDF, BNode, Literal
from rdflib.collection import Collection
from rdflib.compare import isomorphic
from rdflib.plugins.serializers.rdfxml import RDFVOC, PrettyXMLSerializer

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


class LiteralListXMLSerializer(PrettyXMLSerializer):
    """rdflib's pretty RDF/XML, with lists of literals written correctly.

    pretty-xml writes every list as rdf:parseType="Collection", which can only
    hold resources. A list of literals (sh:languageIn in the SHACL shapes) is
    then written as resources and lost. This writes such a list as nested
    rdf:first/rdf:rest blank nodes instead, and leaves everything else to
    rdflib.

    It relies on rdflib internals (the private record of serialised nodes) and
    was written against rdflib 7.6.0. serialise() checks the result by round
    trip, so a change in rdflib makes the output flat, not wrong.
    """

    def predicate(self, predicate, object, depth=1):
        serialised = self._PrettyXMLSerializer__serialized
        if (
            isinstance(object, BNode)
            and object not in serialised
            and (object, RDF.first, None) in self.store
            and any(isinstance(i, Literal) for i in Collection(self.store, object))
        ):
            serialised[object] = 1
            self.writer.push(predicate)
            self.writer.attribute(RDFVOC.parseType, "Resource")
            self.predicate(RDF.first, self.store.value(object, RDF.first), depth + 1)
            self.predicate(RDF.rest, self.store.value(object, RDF.rest), depth + 1)
            self.writer.pop(predicate)
        else:
            super().predicate(predicate, object, depth)


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

    # rdflib warns about every list it writes as a Collection, including the
    # correct ones. The warnings are silenced because the round trip below is
    # the actual check: if it fails, fall back to the flat serialiser.
    buf = BytesIO()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        LiteralListXMLSerializer(g).serialize(buf, encoding="utf-8")
    rdf = buf.getvalue().decode("utf-8")
    if not isomorphic(g, rdflib.Graph().parse(data=rdf, format="xml")):
        rdf = g.serialize(format="xml")
        print(f"  {src.name}: pretty RDF/XML loses triples, using flat RDF/XML")
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

    print("\n== Serialise SHACL shapes ==")
    for f in sorted((REPO_ROOT / "src" / "shaclShapes").glob("*.ttl")):
        serialise(f, dist / "shaclShapes")

    print("\nSerialise Done.")


if __name__ == "__main__":
    main()
