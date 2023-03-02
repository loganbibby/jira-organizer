from pathlib import Path
import environ

env = environ.Env()

DATA_DIR = env.path(
    "DATA_DIR",
    environ.Path(Path(__file__).parent.parent.parent.resolve(), "data")
)

DATA_FILE = env.path(
    "DATA_FILE",
    DATA_DIR.path("data.json")
)

CACHE_TYPE = "FileSystemCache"
CACHE_DIR = env.path(
    "CACHE_DIR",
    DATA_DIR.path("cache")
)
CACHE_DEFAULT_TIMEOUT = env.int(
    "CACHE_TIMEOUT",
    300
)
