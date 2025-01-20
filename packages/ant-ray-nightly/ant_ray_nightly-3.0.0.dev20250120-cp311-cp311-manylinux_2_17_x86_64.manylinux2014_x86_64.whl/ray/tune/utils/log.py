import time
from enum import Enum
from typing import Dict, Tuple, Union

from ray.util import PublicAPI
from ray.util.annotations import DeveloperAPI


@PublicAPI
class Verbosity(Enum):
    V0_MINIMAL = 0
    V1_EXPERIMENT = 1
    V2_TRIAL_NORM = 2
    V3_TRIAL_DETAILS = 3

    def __int__(self):
        return self.value


verbosity: Union[int, Verbosity] = Verbosity.V3_TRIAL_DETAILS


@DeveloperAPI
def set_verbosity(level: Union[int, Verbosity]):
    global verbosity

    if isinstance(level, int):
        verbosity = Verbosity(level)
    else:
        verbosity = level


@DeveloperAPI
def has_verbosity(level: Union[int, Verbosity]) -> bool:
    """Return True if passed level exceeds global verbosity level."""
    global verbosity

    log_level = int(level)
    verbosity_level = int(verbosity)

    return verbosity_level >= log_level


@DeveloperAPI
def disable_ipython():
    """Disable output of IPython HTML objects."""
    try:
        from IPython.core.interactiveshell import InteractiveShell

        InteractiveShell.clear_instance()
    except Exception:
        pass


_log_cache_count: Dict[str, Tuple[str, float]] = {}


def _dedup_logs(domain: str, value: str, repeat_after_s: int = 5) -> bool:
    cur_val, ts = _log_cache_count.get(domain, (None, None))
    if value == cur_val and time.monotonic() - repeat_after_s < ts:
        return False
    else:
        _log_cache_count[domain] = value, time.monotonic()
        return True
