"""Refresh the shareable design runtime from the tested project files (no essays)."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "skills/book-design"
RUNTIME = PACKAGE / "assets/runtime"


def main():
    for directory in ("assets/fonts", "templates"):
        shutil.copytree(ROOT / directory, RUNTIME / directory, dirs_exist_ok=True)
    (RUNTIME / "src").mkdir(parents=True, exist_ok=True)
    (RUNTIME / "config").mkdir(exist_ok=True)
    (RUNTIME / "scripts").mkdir(exist_ok=True)
    for name in ("__init__.py", "settings.py", "print_content.py", "pdf_builder.py"):
        text = (ROOT / "src" / name).read_text(encoding="utf-8")
        if name == "pdf_builder.py":
            start = text.index("SAMPLE =")
            end = text.index("LINK_BASE", start)
            text = text[:start] + "SAMPLE = []\n" + text[end:]
        (RUNTIME / "src" / name).write_text(text, encoding="utf-8")
    (RUNTIME / "src/collection.py").write_text("from pathlib import Path\nROOT = Path(__file__).resolve().parents[1]\n")
    # Reuse ordering, with manuscript-defined sections in the portable adapter.
    text = (ROOT / "src/catalog.py").read_text(encoding="utf-8")
    start = text.index("def validate(")
    end = text.index("def review_text(")
    text = "import math\n\n" + text[start:end]
    text = text.replace("or set(sections) != set(SECTIONS)", "or not sections or any(not isinstance(s, str) or not s.strip() for s in sections)")
    text = text.replace("Section list must contain each of the six sections once.", "Give each manuscript section a unique, nonempty name.")
    (RUNTIME / "src/catalog.py").write_text(text.rstrip() + "\n", encoding="utf-8")
    shutil.copy2(ROOT / "scripts/check_pdf.py", RUNTIME / "scripts/check_pdf.py")
    shutil.copy2(ROOT / "config/reading-defaults.json", RUNTIME / "config/reading-defaults.json")
    shutil.copy2(ROOT / "requirements.txt", RUNTIME / "requirements.txt")
    print("Prepared runtime:", RUNTIME)


if __name__ == "__main__":
    main()
