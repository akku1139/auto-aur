#!/bin/bash
echo "**** starting tidyup.sh ****"
# https://github.com/NobuoTsukamoto/my_actions_test/blob/main/.github/workflows/test_contains.yml
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
  -yq || true
dpkg -r packages-microsoft-prod　> /dev/null 2>&1 || true
apt-get autoremove -y > /dev/null 2>&1 || true
apt-get autoclean -y > /dev/null 2>&1 || true
apt list --installed
rm -rf /home/work/* /var/* /opt/* /usr/local || true
rm -rf "/usr/share/dotnet" || true
rm -rf "$AGENT_TOOLSDIRECTORY" || true
rm -rf "/usr/lib/jvm" || true
rm -rf "/usr/share/swift" || true
rm -rf "/usr/share/kotlinc" || true
rm -rf "/usr/share/miniconda" || true
rm -rf "/usr/share/sbt" || true
rm -rf "/usr/bin/yq" || true
rm -rf "/home/.dotnet/tools" || true
rm -rf "/etc/skel/.dotnet/tools" || true
rm -rf "/home/linuxbrew" || true
rm -rf "/usr/share/apache-maven-3.8.8" || true
rm -rf "/usr/share/gradle-8.7" || true
rm -rf "/home/.nvm" || true
rm -rf "/usr/bin/composer" || true
rm -rf "/home/perflog" || true
rm -rf "/usr/libexec/docker/cli-plugins" || true
rm -rf "/usr/bin/docker-credential-ecr-login" || true
echo "**** tidyup.sh done ****"
