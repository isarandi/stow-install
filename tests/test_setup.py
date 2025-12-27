"""Tests for stow-install --setup functionality."""
import os

from .helpers import run_stow_install


def test_setup_creates_directories(fake_home, fake_env):
    """Test that --setup creates the expected directory structure."""
    result = run_stow_install('--setup', env=fake_env, capture_output=True, text=True)
    assert result.returncode == 0

    local_dir = os.path.join(fake_home, '.local')
    assert os.path.isdir(local_dir)

    # Check key directories exist
    expected_dirs = [
        'bin', 'bin_priority', 'lib', 'lib64', 'include', 'share', 'stow',
        'lib/pkgconfig', 'lib64/pkgconfig', 'lib/cmake', 'lib64/cmake',
        'share/man', 'share/info', 'share/applications', 'share/icons',
        'share/bash-completion/completions', 'share/locale'
    ]
    for d in expected_dirs:
        path = os.path.join(local_dir, d)
        assert os.path.isdir(path), f"Expected directory {d} to exist"


def test_setup_creates_bashrc(fake_home, fake_env):
    """Test that --setup adds environment variables to .bashrc."""
    result = run_stow_install('--setup', env=fake_env, capture_output=True, text=True)
    assert result.returncode == 0

    bashrc_path = os.path.join(fake_home, '.bashrc')
    assert os.path.isfile(bashrc_path)

    with open(bashrc_path) as f:
        content = f.read()

    # Check key environment variables are set
    assert 'export STOW_DIR=' in content
    assert 'export PATH=' in content
    assert 'export LD_LIBRARY_PATH=' in content
    assert 'export PKG_CONFIG_PATH=' in content
    assert 'export CMAKE_PREFIX_PATH=' in content
    assert 'export CPATH=' in content
    assert 'export XDG_DATA_DIRS=' in content


def test_setup_creates_stow_global_ignore(fake_home, fake_env):
    """Test that --setup creates ~/.stow-global-ignore."""
    result = run_stow_install('--setup', env=fake_env, capture_output=True, text=True)
    assert result.returncode == 0

    ignore_path = os.path.join(fake_home, '.stow-global-ignore')
    assert os.path.isfile(ignore_path)

    with open(ignore_path) as f:
        content = f.read()

    # Check key patterns
    assert '^/share/info/dir' in content
    assert '\\.git' in content


def test_setup_idempotent(fake_home, fake_env):
    """Test that running --setup twice doesn't duplicate bashrc entries."""
    # Run setup twice
    run_stow_install('--setup', env=fake_env, check=True)
    run_stow_install('--setup', env=fake_env, check=True)

    bashrc_path = os.path.join(fake_home, '.bashrc')
    with open(bashrc_path) as f:
        content = f.read()

    # STOW_DIR should appear only once
    assert content.count('export STOW_DIR=') == 1
