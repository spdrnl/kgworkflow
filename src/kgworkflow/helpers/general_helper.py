import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)


class UserException(Exception):
    pass


def get_project_root() -> Path:
    """
    Returns the root directory of the project.

    This function computes the root directory of the project
    by moving up four levels in the directory structure
    from the current module's absolute path.

    :return: The root directory of the project.
    :rtype: Path
    """
    return Path(os.path.abspath(__file__)).parent.parent.parent.parent
