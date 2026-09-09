# Contributing

This edition is in early development. Read the [current status](docs/progress.md) and [design requirements](docs/design.md) before proposing a change. Windows setup, essay collection and sample PDF output are available; the project uses commands and saved settings, with optional agent assistance.

## Report a problem

Open an issue in [this fork](https://github.com/HarshK99/graham-essays/issues), if issues are enabled, or include the details in a pull request. Include your Windows and Python versions, the command you ran, what you expected, and the error text. Remove private paths or other personal information you do not want to share. Problems with this edition belong here rather than in the original project's issue tracker.

## Propose a change

Use `ipad-reading-edition` as the starting branch and the pull request's destination. Keep changes focused and explain what changed and how you checked it. Follow [AGENTS.md](AGENTS.md) when using a coding assistant.

After changing the Windows foundation, run from the project folder:

```powershell
python scripts/setup_windows.py
.\.venv\Scripts\python.exe run.py
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
git diff --check
```

For setup changes, also install in a fresh copy whose path contains spaces; do not copy an existing `.venv`. Record actual outcomes. Run `.\.venv\Scripts\python.exe scripts/check_windows_pdf_setup.py` for the clean-install sample check, and `scripts/check_pdf.py` with an actual PDF path for export checks. Windows checks do not prove iPad reading quality.

Do not commit downloaded essays, generated books, annotations, personal settings, credentials, or Python environments. The ignore rules cover the current local-data locations. Keep upstream attribution intact and read the [reuse review](docs/upstream/PROVENANCE.md) before adding or distributing third-party assets.
