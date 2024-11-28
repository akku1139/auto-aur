# Show commands
set -x
# Error
set -e

HOME="/home/builder"

mkdir -p $HOME/.cargo $HOME/.config/sccache-dist
# mkdir -p $HOME/.cargo $HOME/.ccache

gpg --allow-secret-key-import --import --batch --yes << EOL
$GPG_PRIVATE_KEY
EOL

cat >> $HOME/.gnupg/gpg.conf << EOL
passphrase $GPG_PASSPHRASE
pinentry-mode loopback
no-tty
EOL

# cat > $HOME/.ccache/ccache.conf << EOL

# EOL

cat > $HOME/.cargo/config.toml << EOL
[build]
rustc-wrapper = "sccache"
EOL

chmod 600 $HOME/.gnupg/gpg.conf
#find $HOME/.gnupg -type f -name "*.lock" | xargs rm -f

cat > $HOME/.ssh/id_tcpexposer.com.pub << EOL
$TCPEXPOSER_PUBLIC_KEY
EOL

cat > /.ssh/id_tcpexposer.com << EOL
$TCPEXPOSER_PRIVATE_KEY
EOL

cat > /.ssh/config << EOL
Host tcpexposer.com
  User aku-2
  HostName tcpexposer.com
  TCPKeepAlive yes
  IdentityFile ~/.ssh/id_tcpexposer.com
  IdentitiesOnly yes
EOL

cat > $HOME/.config/sccache-dist/scheduler-config.toml << EOL
public_addr = "127.0.0.1:10600"

[client_auth]
type = "token"
token = "$SCCACHE_CLIENT_TOKEN"

[server_auth]
type = "token"
token = "$SCCACHE_SERVER_TOKEN"
EOL

cat > $HOME/.config/sccache-dist/server-config.toml << EOL
# This is where client toolchains will be stored.
cache_dir = "/tmp/toolchains"
# The maximum size of the toolchain cache, in bytes.
# If unspecified the default is 10GB.
# toolchain_cache_size = 10737418240
# A public IP address and port that clients will use to connect to this builder.
public_addr = "$SCCACHE_SERVER_ADDR:443"
# The URL used to connect to the scheduler (should use https, given an ideal
# setup of a HTTPS server in front of the scheduler)
scheduler_url = "http://127.0.0.1:10600"

[builder]
type = "overlay"
# The directory under which a sandboxed filesystem will be created for builds.
build_dir = "/tmp/build"
# The path to the bubblewrap version 0.3.0+ `bwrap` binary.
bwrap_path = "/usr/bin/bwrap"

[scheduler_auth]
type = "token"
token = "$SCCACHE_SERVER_TOKEN"
EOL


sccache-dist scheduler --config $HOME/.config/sccache-dist/scheduler-config.toml &
sudo sccache-dist server --config $HOME/.config/sccache-dist/scheduler-config.toml &
