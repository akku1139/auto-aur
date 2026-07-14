FROM archlinux:base-devel

RUN pacman-key --init
RUN pacman-key --recv-key 3056513887B78AEB --keyserver keyserver.ubuntu.com
RUN pacman-key --lsign-key 3056513887B78AEB
RUN pacman --noconfirm -U "https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-keyring.pkg.tar.zst" \
                          "https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-mirrorlist.pkg.tar.zst"

RUN pacman-key --recv-key b465fd29d2ea44cc --keyserver keyserver.ubuntu.com
RUN pacman-key --lsign-key b465fd29d2ea44cc
RUN pacman --noconfirm -U 'https://auto-aur.pages.dev/repo/auto-aur/x86_64/auto-aur-keyring-20240923-1-any.pkg.tar.zst' \
                          'https://auto-aur.pages.dev/repo/auto-aur/x86_64/auto-aur-mirrorlist-20260606-1-any.pkg.tar.zst'

RUN pacman -Syu --noconfirm --needed git sudo unzip

RUN echo -e "[chaotic-aur]\nInclude = /etc/pacman.d/chaotic-mirrorlist" >> /etc/pacman.conf
RUN echo -e "[auto-aur]\nInclude = /etc/pacman.d/auto-aur-mirrorlist" >> /etc/pacman.conf
RUN pacman -Sy

# after every pacman
RUN echo -e "[auto-aur-local]\nServer = file:///repo\nSigLevel = Optional TrustAll" >> /etc/pacman.conf
RUN sed -i '/^OPTIONS=/s/\bdebug\b/!debug/g' /etc/makepkg.conf
RUN sed -i '/^BUILDENV=/s/\bcheck\b/!check/g' /etc/makepkg.conf

RUN useradd -m builder
RUN echo 'builder ALL=(ALL) NOPASSWD: /usr/bin/pacman' >> /etc/sudoers

COPY scripts/build/entry.sh /entry.sh
RUN chmod +x /entry.sh

WORKDIR /home/builder/src
ENTRYPOINT ["/entry.sh"]
