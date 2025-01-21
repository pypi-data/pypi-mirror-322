from pathlib import Path

from importlib_resources import files


def get_include() -> Path:
    return files("libboost_headers.include")
