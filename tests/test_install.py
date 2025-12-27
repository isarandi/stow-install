"""Tests for stow-install installation functionality."""
import os
from pathlib import Path

from .helpers import run_stow_install

FIXTURES_DIR = Path(__file__).parent / 'fixtures'


def test_install_from_local_tarball(setup_home):
    """Test installing from a local .tar.gz file."""
    fake_home, env = setup_home

    tarball = FIXTURES_DIR / 'dummy-1.0.tar.gz'
    result = run_stow_install(
        '--name=dummy-1.0',
        f'--source={tarball}',
        f'--target={fake_home}/.local',
        env=env,
        capture_output=True,
        text=True,
        cwd=fake_home
    )
    assert result.returncode == 0, f"Install failed: {result.stderr}"

    # Check package is in stow directory
    stow_pkg = os.path.join(fake_home, '.local', 'stow', 'dummy-1.0')
    assert os.path.isdir(stow_pkg), "Package not in stow directory"

    # Check binary was installed
    binary = os.path.join(stow_pkg, 'bin', 'dummy')
    assert os.path.isfile(binary), "Binary not found in package"

    # Check symlink was created
    symlink = os.path.join(fake_home, '.local', 'bin', 'dummy')
    assert os.path.islink(symlink), "Symlink not created"


def test_install_from_local_directory(setup_home):
    """Test installing from a local source directory."""
    fake_home, env = setup_home

    source_dir = FIXTURES_DIR / 'dummy-1.0'
    result = run_stow_install(
        '--name=dummy-1.0',
        f'--source={source_dir}',
        f'--target={fake_home}/.local',
        env=env,
        capture_output=True,
        text=True,
        cwd=fake_home
    )
    assert result.returncode == 0, f"Install failed: {result.stderr}"

    # Check binary symlink exists
    symlink = os.path.join(fake_home, '.local', 'bin', 'dummy')
    assert os.path.islink(symlink), "Symlink not created"


def test_install_refuses_duplicate(setup_home):
    """Test that installing the same package twice fails."""
    fake_home, env = setup_home

    tarball = FIXTURES_DIR / 'dummy-1.0.tar.gz'

    # First install should succeed
    result1 = run_stow_install(
        '--name=dummy-1.0',
        f'--source={tarball}',
        f'--target={fake_home}/.local',
        env=env,
        capture_output=True,
        text=True,
        cwd=fake_home
    )
    assert result1.returncode == 0

    # Second install should fail
    result2 = run_stow_install(
        '--name=dummy-1.0',
        f'--source={tarball}',
        f'--target={fake_home}/.local',
        env=env,
        capture_output=True,
        text=True,
        cwd=fake_home
    )
    assert result2.returncode != 0
