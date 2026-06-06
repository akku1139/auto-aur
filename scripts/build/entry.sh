#!/bin/bash

set -ex
chown -R builder:builder /home/builder/src
cd /home/builder/src
sudo -u builder makepkg -s --noconfirm
cp *.pkg.tar.zst /repo/
