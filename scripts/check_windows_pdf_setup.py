"""Exercise setup and sample export in a fresh Windows path containing spaces."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.pdf_builder import SAMPLE


def main():
    with tempfile.TemporaryDirectory(prefix='Reading Edition clean ') as directory:
        root = Path(directory).resolve()
        for name in ('src', 'scripts', 'templates', 'assets/fonts', 'config'):
            shutil.copytree(ROOT / name, root / name, ignore=shutil.ignore_patterns('__pycache__', '*.local.json', 'reading-settings.json'))
        for name in ('requirements.txt', 'run.py', 'cover.png'):
            shutil.copy2(ROOT / name, root / name)
        (root / 'data/sources').mkdir(parents=True)
        shutil.copy2(ROOT / 'data/catalog.json', root / 'data/catalog.json')
        catalog = json.loads((ROOT / 'data/catalog.json').read_text(encoding='utf-8'))
        for record in catalog['essays']:
            if record['id'] in SAMPLE:
                names = [record['source'], record['content']] + [a['source'] for a in record.get('assets', []) if a.get('source')]
                for name in names:
                    shutil.copy2(ROOT / name, root / name)
        subprocess.run([sys.executable, str(root / 'scripts/setup_windows.py')], cwd=root.parent, check=True)
        python = root / '.venv/Scripts/python.exe'
        subprocess.run([str(python), '-m', 'src.pdf_builder'], cwd=root, check=True)
        pdf = next((root / 'output').glob('*.pdf'))
        subprocess.run([str(python), str(root / 'scripts/check_pdf.py'), str(pdf)], cwd=root.parent, check=True)
        print('Fresh Windows setup and sample checks passed in a path containing spaces.')


if __name__ == '__main__':
    main()
