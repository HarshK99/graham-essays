"""Prepare the Windows environment without shell activation or Unix tools."""

from pathlib import Path
import subprocess
import sys
import venv


def main():
    if sys.platform != "win32" or sys.version_info[:2] != (3, 14):
        print("Setup requires Windows and Python 3.14. Run with: py -3.14 scripts/setup_windows.py")
        return 1
    root = Path(__file__).resolve().parents[1]
    environment = root / ".venv"
    python = environment / "Scripts" / "python.exe"
    try:
        if not python.exists():
            print("Creating the project's private Python environment...", flush=True)
            venv.EnvBuilder(with_pip=True).create(environment)
        version = subprocess.check_output(
            [str(python), "-c", "import sys; print('%s.%s' % sys.version_info[:2])"], text=True
        ).strip()
        if version != "3.14":
            print("The existing .venv uses a different Python version. Rename it and rerun setup.")
            return 1
        subprocess.run(
            [str(python), "-m", "pip", "install", "--disable-pip-version-check",
             "--require-hashes", "-r", str(root / "requirements.txt")],
            cwd=root, check=True,
        )
        subprocess.run([str(python), '-m', 'playwright', 'install', 'chromium'], cwd=root, check=True)
        return subprocess.run([str(python), str(root / "run.py")], cwd=root).returncode
    except (OSError, subprocess.CalledProcessError) as error:
        print(f"Setup did not finish: {error}")
        print("Check Python and internet access, then rerun the same setup command.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
