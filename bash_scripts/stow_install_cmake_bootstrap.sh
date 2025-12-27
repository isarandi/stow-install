#!/usr/bin/env bash
# Usage: cd to the CMake source directory, then run:
#   stow_install_cmake_bootstrap.sh <package-name> [bootstrap-args...]
#
# For building CMake itself without an existing cmake installation.
#
set -euo pipefail

PACKAGE_NAME=$1
shift

TARGET=$HOME/.local

./bootstrap --prefix="$TARGET" --parallel="$(nproc)" -- "$@"
make -j "$(nproc)"

TEMP_DESTDIR=$(mktemp --directory --tmpdir="$STOW_DIR")
make install DESTDIR="$TEMP_DESTDIR"
mv -T "$TEMP_DESTDIR/$TARGET" "$STOW_DIR/$PACKAGE_NAME"
rm -rf "$TEMP_DESTDIR"
stow "$PACKAGE_NAME" --target="$TARGET"
