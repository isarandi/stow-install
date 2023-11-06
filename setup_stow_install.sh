mkdir -p ~/.local
pushd ~/.local
mkdir -p bin_priority bin doc etc games include info lib lib/pkgconfig lib32 lib64 libexec libx32 man sbin share share/aclocal share/man src stow var
popd

echo '' >> ~/.bashrc
cat .bashrc_stow >> ~/.bashrc
cp stow-install ~/.local/bin_priority/
