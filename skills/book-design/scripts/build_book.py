"""Build and audit an original manuscript in a separate working folder."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import sys

PACKAGE = Path(__file__).resolve().parents[1]
RUNTIME = PACKAGE / "assets/runtime"
sys.path.insert(0, str(RUNTIME))
from src.pdf_builder import build
from src.settings import load
from scripts.check_pdf import check


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manuscript", type=Path)
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--settings", type=Path)
    args = parser.parse_args()
    manuscript = json.loads(args.manuscript.read_text(encoding="utf-8-sig"))
    root = args.workspace.resolve()
    # Keep packaged resources read-only; each exercise gets a new workspace.
    root.mkdir(parents=True, exist_ok=False)
    for folder in ("assets", "templates", "config"):
        shutil.copytree(RUNTIME / folder, root / folder)
    (root / "data/sources").mkdir(parents=True)
    book = {key: manuscript[key] for key in ("title", "author", "source_credit", "sections")}
    book["essays"] = {}
    records = []
    for index, chapter in enumerate(manuscript["chapters"]):
        key = chapter["id"]
        if key in book["essays"]:
            raise ValueError("Repeated chapter ID: " + key)
        raw = chapter["html"].encode("utf-8")
        digest = hashlib.sha256(raw).hexdigest()
        relative = "data/sources/" + digest + ".html"
        (root / relative).write_bytes(raw)
        records.append(dict(id=key, title=chapter["title"], url="https://example.invalid/chapter/" + key,
                            date=manuscript.get("date"), source_order=index, status="success",
                            source=relative, content=relative, sha256=digest, assets=[],
                            retrieved_at=datetime.now(timezone.utc).isoformat()))
        book["essays"][key] = dict(section=chapter["section"], included=True, order=index)
    (root / "data/catalog.json").write_text(json.dumps({"essays": records}), encoding="utf-8")
    (root / "config/book.json").write_text(json.dumps(book), encoding="utf-8")
    pdf = build(root=root, settings=load(args.settings, root=root), full=True)
    report = check(pdf, root=root)
    print(json.dumps(dict(pdf=str(pdf), pages=report["pages"], issues=report["issues"]), indent=2))
    return int(bool(report["issues"]))


if __name__ == "__main__":
    raise SystemExit(main())
