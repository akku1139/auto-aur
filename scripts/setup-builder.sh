# Show commands
set -x
# Error
set -e

HOME="/home/builder"

mkdir -p $HOME/.cargo $HOME/.config/sccache-dist $HOME/.ssh
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

cat >> /.ssh/config << EOL
Host tcpexposer.com
  User aku-2
  HostName tcpexposer.com
  TCPKeepAlive yes
  IdentityFile ~/.ssh/id_tcpexposer.com
  IdentitiesOnly yes
EOL

cat >> ~/.ssh/known_hosts << EOL
# tcpexposer.com:22 SSH-2.0-sish
|1|PWKuAKfpfTyXmLUOlXZX2W+7C8Y=|pdbC3oKKs4H7lSgFHODZGyj1JuU= ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIF9qb8hhyV/kBYq/X00tsnsbKdT5bXli5MN2frvtHqdw
# tcpexposer.com:22 SSH-2.0-sish
|1|GQBsQinK5IywjROSdpa1Lliczi0=|pRvgj+90jrTLEiqUvoSoL2syr9A= ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCeuHC9irjuXnBGa6ZxHYAgu93rrzLYT37RxTubXo9HInJwfqZZ5z2OJFgVt3hc5tTr1Nt6ozkDMrG/p1U2teAX+aRUZ0CyEbUGofChU8n9ZEDv3S+VIIUMfAXn966nIUVjai2gmcRnENl8i0KZ5YRjS5UTmvz15N4RfhA8p0vltHwTOo4z86aRHuHI5M1f5g2GX4TU2zp+BR0T6qJiSGFLHqZsNgZ1NVwwyNOFY5IbkqxywmLwwU4jQXhoiVpJsI+ylzWdvS4EhXjbAlYSb13yajiXYNNlEVLb+IPyAvjsIUXe7cPvjrWMW8ZSvHUehCRPKz/BApQJSbF9Dqq72B+e8WRf1TGN2tDKh7ew/eBVmQtGfjPsytulPH5RnhFw6gpIla0r+sV/rLRmsYpRG4/T22LvbDVRd88C2kgnF18MlErKH1k0jSOZ87vVYASQ4Rbr8WAY/AHMwpZErX7Ql5g+4Hg0YDM8Y/TqT1h8y/VocanBAgOHfUr5O9SnCX9CmuE=
# tcpexposer.com:22 SSH-2.0-sish
# tcpexposer.com:22 SSH-2.0-sish
# tcpexposer.com:22 SSH-2.0-sish
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

cat > $HOME/.config/sccache/config << EOL
[dist]
# The URL used to connect to the scheduler (should use https, given an ideal
# setup of a HTTPS server in front of the scheduler)
scheduler_url = "http://127.0.0.1:10600"
# Used for mapping local toolchains to remote cross-compile toolchains. Empty in
# this example where the client and build server are both Linux.
toolchains = []
# Size of the local toolchain cache, in bytes (5GB here, 10GB if unspecified).
toolchain_cache_size = 5368709120

[dist.auth]
type = "token"
# This should match the `client_auth` section of the scheduler config.
token = "$SCCACHE_CLIENT_TOKEN"
EOL

ssh $SCCACHE_SCHEDULER_ADDR:80:localhost:10600 aku-2@tcpexposer.com &

sccache-dist scheduler --config $HOME/.config/sccache-dist/scheduler-config.toml &
sudo sccache-dist server --config $HOME/.config/sccache-dist/scheduler-config.toml &
