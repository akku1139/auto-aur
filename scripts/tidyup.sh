#!/bin/bash -x

echo "**** starting tidyup.sh ****"
set -x

# https://github.com/NobuoTsukamoto/my_actions_test/blob/main/.github/workflows/test_contains.yml
npm uninstall bazel
npm uninstall bazelisk
rustup self uninstall -y
apt purge \
  ansible \
  aria2 \
  azure-cli \
  cabal* \
  clang* \
  dotnet-sdk* \
  ghc* \
  google-chrome-stable \
  kubectl \
  mysql* \
  node* \
  npm* \
  php* \
  powershell \
  rpm \
  ruby* \
  subversion \
  yarn \
  firefox \
  mono-complete \
  nuget \
  apache2 \
  moby-engine \
  moby-cli \
  moby-buildx \
  moby-compose \
  microsoft-edge-stable \
  mongodb* \
  nginx \
  postgresql* \
  libpq-dev \
  r-base \
  sphinxsearch \
  swig \
  tcl \
  temurin-* \
  skopeo \
  imagemagick-* \
  mssql-tools* \
  unixodbc-dev \
  ubuntu-advantage-tools \
  docker-* \
  fonts-* \
  llvm-* \
  javascript-common \
  openjdk-11-jre-headless \
  linux-cloud-tools* \
  linux-azure-6.2-* \
  hicolor-icon-theme \
  gcc-9 \
  gcc-10 \
  gcc-11 \
  gcc-12 \
  cloud-initramfs* \
  x11-* \
  bind9-* \
  cloud-* \
  gir1.2-* \
  golang-github-* \
  libjs-* \
  libllvm* \
  nano \
  python3-* \
  podman \
  buildah \
  skopeo \
  temurin-* \
  ant \
  ant-optional \
  libmysqlclient-dev \
  libxft-dev \
  libfreetype6-dev \
  libfontconfig1-dev \
  libpq-dev \
  tcl* \
  p7zip* \
  gfortran-13 \
  gcc-12-* \
  gcc-11-* \
  google-cloud-cli \
  heroku \
  snmp \
  liblz4-dev \
  man-db \
  packages-microsoft-prod \
  perl \
  *-dev \
  linux-headers-* \
  manpages \
  -yq > /dev/null 2>&1
dpkg -r packages-microsoft-prod　> /dev/null 2>&1
apt-get autoremove -y > /dev/null 2>&1
apt-get autoclean -y > /dev/null 2>&1
#apt list --installed
rm -rf "/home/work/*"
rm -rf "/opt/*"
rm -rf "/usr/local/*"
rm -rf "/usr/share/dotnet"
rm -rf "$AGENT_TOOLSDIRECTORY"
rm -rf "/usr/lib/jvm"
rm -rf "/usr/share/swift"
rm -rf "/usr/share/kotlinc"
rm -rf "/usr/share/miniconda"
rm -rf "/usr/share/sbt"
rm -rf "/usr/bin/yq"
rm -rf "/home/.dotnet/tools"
rm -rf "/etc/skel/.dotnet/tools"
rm -rf "/home/linuxbrew"
rm -rf "/usr/share/apache-maven-3.8.8"
rm -rf "/usr/share/gradle-8.7"
rm -rf "/home/.nvm"
rm -rf "/usr/bin/composer"
rm -rf "/home/perflog"
rm -rf "/usr/libexec/docker/cli-plugins"
rm -rf "/usr/bin/docker-credential-ecr-login"

set +x
echo "**** tidyup.sh done ****"
