# Stow-Install

You often don't have root access on a shared machine, like a compute cluster, but you still want to install software.
GNU Stow makes it easy to install and uninstall self-compiled programs and libraries in your home folder.

This tool makes this even easier by handling **the download, the compilation and the installation** for you, in simple cases as easily as a `pip install`.

## Installation

```bash
pip install stow-install
```

Then run `stow-install --setup` to create the `~/.local` directory structure and to add environment variables to your `.bashrc`. Finally start a new shell session or `source ~/.bashrc` to activate the changes.

You can also directly download the `stow-install` script and run it from anywhere or place it in a directory in your `$PATH`.


## Usage

To install a program or library, you need to provide a name for it and a source (filename, source directory path or URL). For example, to install an up-to-date version of CMake, you can run:

```bash
stow-install --name=cmake-3.27 --source=https://github.com/Kitware/CMake/releases/download/v3.27.7/cmake-3.27.7.tar.gz
```

This should download, extract, compile and stow CMake, so that the `cmake` command will use this newly installed version.

You can also specify compilation config arguments that will be passed to `./configure` or `cmake`, for example, to build a new version of GCC, you can run (notice the arguments after the `--`, they will be passed to `./configure`):

```bash
LOCAL=$HOME/.local

stow-install --name=gmp-6.3 --source=https://gmplib.org/download/gmp/gmp-6.3.0.tar.xz -- --enable-static --enable-shared
stow-install --name=mpfr-4.2 --source=https://www.mpfr.org/mpfr-current/mpfr-4.2.1.tar.xz -- --with-gmp=$LOCAL
stow-install --name=mpc-1.3 --source=https://ftp.gnu.org/gnu/mpc/mpc-1.3.1.tar.gz -- --with-gmp=$LOCAL --with-mpfr=$LOCAL
stow-install --name=gcc-11.3 --source=https://ftp.gwdg.de/pub/misc/gcc/releases/gcc-11.3.0/gcc-11.3.0.tar.gz -- --with-gmp=$LOCAL --with-mpfr=$LOCAL --with-mpc=$LOCAL --disable-multilib
```

stow-install auto-detects the build system (CMake, Autotools, Meson, or plain Makefile).

## Manual intervention

Sometimes the automated process breaks down somewhere, and you may want to manually fix things.
For this, useful commands are given in the `bash_scripts` directory to perform command by command what the automatic tool would do.

# Background
## What's Stow and why is it good?
If you compile and install a lot of software into your home without using stow (or a similar tool), you end up with a bunch of files in the bin, lib etc. folders and no way of knowing which file was put there by which piece of software. This makes it difficult to remove installations if it turns out that you don't need or like the library anymore or you want to use a different version.

GNU Stow is a "symbolic link farm". All your software installations physically live under a separate ~/.local/stow/name-of-the-library folder, and Stow creates symbolic links in ~/.local/bin, ~/.local/lib etc. When you need to uninstall software X, Stow will simply search for symlinks that point into ~/.local/stow/X/ and delete them.

This package uses [stow-python](https://github.com/isarandi/stow-python), my Python reimplementation of GNU Stow, so no Perl dependency is required.
