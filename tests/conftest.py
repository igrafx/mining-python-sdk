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
# This patch safely handles None values by returning 0 instead of crashing.

# Save the original lineno property getter function
_original_lineno_fget = _pytest_code.TracebackEntry.lineno.fget


@property
def _safe_lineno(self):
    """
    Safe lineno property that handles None tb_lineno values.
    This function fixes the TypeError: unsupported operand type(s) for -: 'NoneType' and 'int'
    that occurs when pytest-dependency 0.6.1 interacts with pytest 8.x and pluggy 1.6.0.
    Args:
        self: The TracebackEntry instance
    Returns:
        int: The line number (0 if tb_lineno is None, otherwise the actual line number)
    """
    raw = self._rawentry.tb_lineno
    if raw is None:
        # Return 0 instead of None to prevent subtraction error in traceback formatting
        return 0
    return _original_lineno_fget(self)


# Patch the TracebackEntry.lineno property with our safe version
_pytest_code.TracebackEntry.lineno = _safe_lineno


def pytest_configure():
    """Configure workgroup and project as pytest fixtures."""
    pytest.workgroup = None
    pytest.project = None
