import sys

from datetime import datetime, timedelta, timezone
from importlib.metadata import version

from pathlib import Path

HOME_DIR = Path.home() / ".fpk"
HOME_DIR.mkdir(exist_ok=True)
PACKAGE_DIR = Path(sys.modules["flatpack"].__file__).parent
CONFIG_FILE_PATH = HOME_DIR / ".fpk_config.toml"
GITHUB_CACHE = HOME_DIR / ".fpk_github.cache"
IMPORT_CACHE_FILE = PACKAGE_DIR / ".fpk_import_cache"

BASE_URL = "https://raw.githubusercontent.com/RomlinGroup/Flatpack/main/warehouse"
GITHUB_REPO_URL = "https://api.github.com/repos/RomlinGroup/Flatpack"
TEMPLATE_REPO_URL = "https://api.github.com/repos/RomlinGroup/template"

CONNECTIONS_FILE = "connections.json"
HOOKS_FILE = "hooks.json"

COOLDOWN_PERIOD = timedelta(minutes=1)
GITHUB_CACHE_EXPIRY = timedelta(hours=1)
SERVER_START_TIME = None

CSRF_EXEMPT_PATHS = ["/", "/csrf-token", "/favicon.ico", "/static"]

MAX_ATTEMPTS = 5
VALIDATION_ATTEMPTS = 0

VERSION = version("flatpack")
