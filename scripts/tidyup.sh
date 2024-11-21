#!/bin/bash -x
echo "**** starting tidyup.sh ****"
set -x
# https://github.com/NobuoTsukamoto/my_actions_test/blob/main/.github/workflows/test_contains.yml
npm uninstall bazel || true
npm uninstall bazelisk || true
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
  -yq > /dev/null 2>&1 || true
dpkg -r packages-microsoft-prod　> /dev/null 2>&1 || true
apt-get autoremove -y > /dev/null 2>&1 || true
apt-get autoclean -y > /dev/null 2>&1 || true
#apt list --installed
rm -rf "/home/work/*" || true
rm -rf "/opt/*" || true
rm -rf "/usr/share/dotnet" || true
rm -rf "$AGENT_TOOLSDIRECTORY" || true
rm -rf "/usr/local/lib/android" || true
rm -rf "/usr/local/share/boost" || true
rm -rf "/usr/lib/jvm" || true
rm -rf "/usr/share/swift" || true
rm -rf "/usr/local/julia*" || true
rm -rf "/usr/share/kotlinc" || true
rm -rf "/usr/local/share/edge_driver" || true
rm -rf "/usr/local/share/chromedriver-linux64" || true
rm -rf "/usr/local/share/gecko_driver" || true
rm -rf "/usr/share/miniconda" || true
rm -rf "/usr/local/share/phantomjs*" || true
rm -rf "/usr/share/sbt" || true
rm -rf "/usr/local/sqlpackage" || true
rm -rf "/usr/bin/yq" || true
rm -rf "/usr/local/share/vcpkg" || true
rm -rf "/usr/local/bin/terraform" || true
rm -rf "/usr/local/bin/stack" || true
rm -rf "/usr/local/bin/aliyun" || true
rm -rf "/usr/local/bin/pulumi" || true
rm -rf "/usr/local/bin/pulumi-language-dotnet" || true
rm -rf "/usr/local/bin/azcopy" || true
rm -rf "/usr/local/aws-cli" || true
rm -rf "/usr/local/bin/bicep" || true
rm -rf "/usr/local/bin/rebar3" || true
rm -rf "/usr/local/bin/phpunit" || true
rm -rf "/usr/local/bin/packer" || true
rm -rf "/usr/local/bin/bicep" || true
rm -rf "/usr/local/bin/docker-compose" || true
rm -rf "/home/.dotnet/tools" || true
rm -rf "/etc/skel/.dotnet/tools" || true
rm -rf "/usr/local/bin/minikube" || true
rm -rf "/usr/local/bin/kustomize" || true
rm -rf "/usr/local/bin/kubectl" || true
rm -rf "/usr/local/bin/kind" || true
rm -rf "/usr/local/bin/helm" || true
rm -rf "/home/linuxbrew" || true
rm -rf "/usr/share/apache-maven-3.8.8" || true
rm -rf "/usr/share/gradle-8.7" || true
rm -rf "/usr/local/share/phantomjs-8.6" || true
rm -rf "/usr/local/bin/azcopy_11.3.1" || true
rm -rf "/usr/local/bin/bicep" || true
rm -rf "/usr/local/bin/.ghcup" || true
rm -rf "/usr/local/.ghcup" || true
rm -rf "/home/.nvm" || true
rm -rf "/usr/bin/composer" || true
rm -rf "/usr/local/bin/phpunit" || true
rm -rf "/usr/local/bin/pulumi-analyzer-policy" || true
rm -rf "/usr/local/bin/pulumi-analyzer-policy-python" || true
rm -rf "/usr/local/bin/pulumi-language-java" || true
rm -rf "/usr/local/bin/pulumi-language-nodejs" || true
rm -rf "/usr/local/bin/pulumi-language-go" || true
rm -rf "/usr/local/bin/pulumi-language-python" || true
rm -rf "/usr/local/bin/pulumi-language-python-exec" || true
rm -rf "/usr/local/bin/pulumi-language-yaml" || true
rm -rf "/usr/local/bin/pulumi-resource-pulumi-nodejs" || true
rm -rf "/usr/local/bin/pulumi-resource-pulumi-python" || true
rm -rf "/usr/local/bin/pulumi-watch" || true
rm -rf "/usr/local/bin/oc" || true
rm -rf "/usr/local/bin/ctest" || true
rm -rf "/usr/local/bin/cmake-gui" || true
rm -rf "/usr/local/bin/ccmake" || true
rm -rf "/usr/local/bin/cpack" || true
rm -rf "/usr/local/bin/oras" || true
rm -rf "/usr/local/share/emacs" || true
rm -rf "/usr/local/share/fonts" || true
rm -rf "/usr/local/share/icons" || true
rm -rf "/usr/local/share/man" || true
rm -rf "/usr/local/share/chromium" || true
rm -rf "/usr/local/share/powershell" || true
rm -rf "/usr/local/share/doc" || true
rm -rf "/home/perflog" || true
rm -rf "/usr/libexec/docker/cli-plugins" || true
rm -rf "/usr/bin/docker-credential-ecr-login" || true
rm -rf "/usr/local/lib/lein" || true
set +x
echo "**** tidyup.sh done ****"
