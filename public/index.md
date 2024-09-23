# Auto-AUR

Pre-built AUR packages.

## Setup

1. Setup Chotic AUR (recommend)

See https://aur.chaotic.cx/docs

Auto-AUR was created to complement Chaotic-AUR.

Auto-AUR packages may depend on other AUR packages.

In that case, Chaotic-AUR provides the necessary pre-built AUR packages.

2. Run commands (root)

```stylus
pacman-key --recv-key b465fd29d2ea44cc --keyserver keyserver.ubuntu.com
pacman-key --lsign-key b465fd29d2ea44cc
pacman -U 'https://auto-aur.pages.dev/repo/auto-aur/x86_64/auto-aur-keyring.pkg.tar.zst'
pacman -U 'https://auto-aur.pages.dev/repo/auto-aur/x86_64/auto-aur-mirrorlist.pkg.tar.zst'
```

3. Edit `/etc/pacman.conf`

Append (adding at the end) the following to `/etc/pacman.conf`:

```ini
[auto-aur]
Include = /etc/pacman.d/auto-aur-mirrorlist
```

## View the latest build log

https://github.com/akku1139/auto-aur/actions
