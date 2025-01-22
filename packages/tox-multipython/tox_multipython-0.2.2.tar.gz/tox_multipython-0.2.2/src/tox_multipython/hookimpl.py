from __future__ import print_function
import logging
import os
import re
import sys
from subprocess import check_output

import pluggy

try:
    from typing import TYPE_CHECKING
except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
    # ruff: noqa: F401 = Union is actually used for typing below
    from typing import Union


# debug logging

DEBUG = bool(os.environ.get('MULTIPYTHON_DEBUG', False))
if DEBUG:
    try:
        from loguru import logger
    except ImportError:
        logging.basicConfig(level=logging.DEBUG)
        logger = logging  # type: ignore

    debug = logger.debug
    exception = logger.exception


hookimpl = pluggy.HookimplMarker('tox')

RX = (
    re.compile(r'^(?P<impl>py)(?P<maj>[23])(?P<min>[0-9][0-9]?)$'),
    re.compile(r'^(?P<impl>py)(?P<maj>3)(?P<min>[0-9][0-9])(?P<suffix>t)$'),
)


@hookimpl
def tox_get_python_executable(envconfig):  # type: ignore
    """Return a python executable for the given python base name."""
    if DEBUG:
        debug('Requested Python executable: {}'.format(envconfig.__dict__))
    path = None
    for rx in RX:
        match = rx.match(envconfig.envname)
        if match is not None:
            if DEBUG:
                debug('Candidate tag: {}'.format(envconfig.envname))
            path = get_python_path(envconfig.envname)
            break
    if path:
        if DEBUG:
            debug('Found Python executable: {}'.format(path))
        return path
    else:
        debug('Failed to propose Python executable')
        return None


def get_python_path(tag):  # type: (str) -> Union[str, None]
    # get path
    try:
        # ruff: noqa: S603 = allow check_output with arbitrary cmdline
        # ruff: noqa: S607 = py is on path, specific location is not guaranteed
        out = check_output(['py', 'bin', '--path', tag])
        enc = sys.getfilesystemencoding()
        path = (out.decode() if enc is None else out.decode(enc)).strip()
        if not path:
            return None
    except Exception:
        exception('Failed to call "py bin --path {}"'.format(tag))
        return None
    return path
