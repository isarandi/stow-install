#!/usr/bin/env bash
# Usage: cd to the source directory, then run:
#   stow_install_make.sh <package-name>
#
# For projects with just a Makefile (no configure/cmake/meson).
#
set -euo pipefail

PACKAGE_NAME=$1

TARGET=$HOME/.local

make -j "$(nproc)" PREFIX="$TARGET"

TEMP_DESTDIR=$(mktemp --directory --tmpdir="$STOW_DIR")
make install DESTDIR="$TEMP_DESTDIR" PREFIX="$TARGET"
mv -T "$TEMP_DESTDIR/$TARGET" "$STOW_DIR/$PACKAGE_NAME"
rm -rf "$TEMP_DESTDIR"
stow "$PACKAGE_NAME" --target="$TARGET"
