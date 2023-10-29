#!/usr/bin/env bash
# Usage: cd to the folder of the source code and then
# stow_install_meson.sh software-name-here
#
set -euo pipefail

PACKAGE_NAME=$1
shift

TARGET=$HOME/.local

mkdir build
cd build
meson ..
meson configure -D prefix="$TARGET" "$@"
ninja -j $(nproc)

TEMP_DESTDIR=$(mktemp --directory --tmpdir="$STOW_DIR")
DESTDIR=$TEMP_DESTDIR ninja install
mv -T "$TEMP_DESTDIR/$TARGET" "$STOW_DIR/$PACKAGE_NAME"
rm -rf "$TEMP_DESTDIR"
stow "$PACKAGE_NAME" --target="$TARGET"
