# MIT License, Copyright 2023 iGrafx
# https://github.com/igrafx/mining-python-sdk/blob/dev/LICENSE
from pathlib import Path
import pytest
from dotenv import load_dotenv
import _pytest._code.code as _pytest_code


dotenv_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path)

# Workaround for pytest-dependency incompatibility with pluggy 1.6.0:
# When pytest-dependency's hookwrapper re-raises exceptions via outcome.get_result(),
# traceback entries can have tb_lineno = None, causing TypeError in repr_traceback_entry.
_original_lineno_fget = _pytest_code.TracebackEntry.lineno.fget


@property
def _safe_lineno(self):
    raw = self._rawentry.tb_lineno
    if raw is None:
        return 0
    return _original_lineno_fget(self)


_pytest_code.TracebackEntry.lineno = _safe_lineno


def pytest_configure():
    """Configure workgroup and project as pytest fixtures."""
    pytest.workgroup = None
    pytest.project = None
