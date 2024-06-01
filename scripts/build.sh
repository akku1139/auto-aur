#!/bin/sh
cat packages.txt | xargs sudo -u nobody paru --noconfirm -S
