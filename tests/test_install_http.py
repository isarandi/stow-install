"""Tests for stow-install HTTP download functionality.

These tests require network access and are marked as slow.
Run with: pytest -m slow
"""
import os

import pytest

from .helpers import run_stow_install


@pytest.mark.slow
def test_install_from_http(setup_home):
    """Test installing from HTTP URL (sic - simple IRC client, ~10KB)."""
    fake_home, env = setup_home

    # sic is a tiny IRC client from suckless.org (~10KB source)
    url = 'https://dl.suckless.org/tools/sic-1.3.tar.gz'

    result = run_stow_install(
        '--name=sic-1.3',
        f'--source={url}',
        f'--target={fake_home}/.local',
        env=env,
        capture_output=True,
        text=True,
        cwd=fake_home,
        timeout=120
    )
    assert result.returncode == 0, f"Install failed: {result.stderr}"

    # Check package is in stow directory
    stow_pkg = os.path.join(fake_home, '.local', 'stow', 'sic-1.3')
    assert os.path.isdir(stow_pkg), "Package not in stow directory"

    # Check binary symlink was created
    symlink = os.path.join(fake_home, '.local', 'bin', 'sic')
    assert os.path.islink(symlink), "Symlink not created"
