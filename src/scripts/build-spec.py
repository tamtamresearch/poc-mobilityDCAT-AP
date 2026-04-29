#!/usr/bin/env python3
"""Build ReSpec spec to dist/index.html.

Serves the repo via a temporary HTTP server so respec's headless browser
can resolve data-include paths (file:// protocol is blocked by Chromium).
Run from repo root: python src/scripts/build-spec.py
"""

import functools
import http.server
import socket
import subprocess
import sys
import threading
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("", 0))
        return s.getsockname()[1]


def main() -> None:
    port = _free_port()
    handler = functools.partial(
        http.server.SimpleHTTPRequestHandler,
        directory=str(REPO_ROOT),
    )
    server = http.server.HTTPServer(("localhost", port), handler)

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    print(f"Serving repo on http://localhost:{port}")

    (REPO_ROOT / "dist").mkdir(exist_ok=True)

    result = subprocess.run(
        [
            "respec",
            "--src", f"http://localhost:{port}/src/index.html",
            "--out", str(REPO_ROOT / "dist" / "index.html"),
        ],
        shell=(sys.platform == "win32"),
    )

    server.shutdown()
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
