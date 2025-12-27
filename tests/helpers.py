"""Test helpers for stow-install tests."""
import subprocess
import sys
from pathlib import Path


def get_stow_install_path():
    """Get path to stow-install in the current venv."""
    # Find stow-install in the same bin directory as the Python interpreter
    venv_bin = Path(sys.executable).parent
    stow_install = venv_bin / 'stow-install'
    if stow_install.exists():
        return str(stow_install)
    # Fallback to which
    import shutil
    return shutil.which('stow-install')


STOW_INSTALL_PATH = get_stow_install_path()


def run_stow_install(*args, env=None, **kwargs):
    """Run stow-install from the test environment."""
    cmd = [sys.executable, STOW_INSTALL_PATH, *args]
    return subprocess.run(cmd, env=env, **kwargs)
