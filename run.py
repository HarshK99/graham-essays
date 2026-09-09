"""Offline Phase 1 readiness check; later phases add collection and app commands."""

import hashlib
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
COVER_SHA256 = "fe6dd55d10b385ba423c3e3852e80f9885895c63451beae1a26c04403f7b9155"


def main():
    if sys.platform != "win32" or sys.version_info[:2] != (3, 14):
        print("Use Windows with Python 3.14 and run scripts/setup_windows.py first.")
        return 1
    if Path(sys.prefix).resolve() != (ROOT / ".venv").resolve():
        print(r"Use the project environment: .\.venv\Scripts\python.exe run.py")
        return 1
    try:
        import requests
        from bs4 import BeautifulSoup

        assert BeautifulSoup("<p>Reading &amp; writing</p>", "html.parser").p.text == "Reading & writing"
        assert requests.Request("GET", "https://paulgraham.com/articles.html").prepare().url
        for name in ("requests", "beautifulsoup4"):
            print(f"Available: {name} {version(name)}")
        cover = ROOT / "cover.png"
        if hashlib.sha256(cover.read_bytes()).hexdigest() != COVER_SHA256:
            raise ValueError("The preserved upstream cover is missing or changed.")
        for relative in ("data/sources", "config", "output"):
            folder = ROOT / relative
            folder.mkdir(parents=True, exist_ok=True)
            with tempfile.TemporaryFile(dir=folder) as probe:
                probe.write(b"readiness check")
            print(f"Ready: {folder}")
    except (ImportError, PackageNotFoundError, OSError, ValueError, AssertionError) as error:
        print(f"Readiness check failed: {error}")
        print("Run: python scripts/setup_windows.py")
        return 1
    print("Windows foundation ready. Use python -m src.collection for sources, or python -m src.pdf_builder for a sample. The browser app is planned for Phase 4.")
    print("Original cover preserved; reuse permission remains unconfirmed. See docs/upstream/PROVENANCE.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
