from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
RESOURCE = PROJECT_ROOT / "resources"
FILE_DIR = RESOURCE / "files"
PEM_DIR = RESOURCE / "pem"

FILES = dict(
    f_50KB=FILE_DIR / "50KB.jpg",
    f_100KB=FILE_DIR / "100KB.jpg",
    f_1MB=FILE_DIR / "1MB.jpg",
    f_5MB=FILE_DIR / "5MB.jpg",
    f_10MB=FILE_DIR / "10MB.pdf",
    f_50MB=FILE_DIR / "50MB.pdf",
    f_100MB=FILE_DIR / "100MB.pdf",
)