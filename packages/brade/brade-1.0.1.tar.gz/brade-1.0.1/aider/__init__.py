try:
    from aider.__version__ import __version__  # type: ignore[import-not-found]
except Exception:
    __version__ = "0.60.1"

__all__ = [__version__]
