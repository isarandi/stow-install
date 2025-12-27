"""Pytest configuration for stow-install tests."""
import os
import tempfile

import pytest

from .helpers import run_stow_install


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (requiring network, deselect with '-m \"not slow\"')"
    )


@pytest.fixture
def fake_home():
    """Create a fake home directory for testing."""
    with tempfile.TemporaryDirectory() as tmp:
        yield tmp


@pytest.fixture
def fake_env(fake_home):
    """Create environment with fake HOME."""
    return {**os.environ, 'HOME': fake_home}


@pytest.fixture
def setup_home(fake_home, fake_env):
    """Set up a fake home with stow-install --setup."""
    result = run_stow_install('--setup', env=fake_env, capture_output=True, text=True)
    assert result.returncode == 0, f"Setup failed: {result.stderr}"
    fake_env['STOW_DIR'] = os.path.join(fake_home, '.local', 'stow')
    return fake_home, fake_env
