#!/usr/bin/env bash
# Usage: cd to the folder of the source code and then
# stow_install_cmake.sh software-name-here
#
set -euo pipefail

PACKAGE_NAME=$1
shift

TARGET=$HOME/.local

mkdir -p build
cd build

cmake -DCMAKE_INSTALL_PREFIX="$TARGET" "$@" ..
make -j $(nproc)

TEMP_DESTDIR=$(mktemp --directory --tmpdir="$STOW_DIR")
make install DESTDIR="$TEMP_DESTDIR"
mv -T "$TEMP_DESTDIR/$TARGET" "$STOW_DIR/$PACKAGE_NAME"
rm -rf "$TEMP_DESTDIR"
stow "$PACKAGE_NAME" --target="$TARGET"

