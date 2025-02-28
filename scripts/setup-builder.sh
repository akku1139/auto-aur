# Show commands
set -x
# Error
set -e

git config --global --add safe.directory /__w/auto-aur/auto-aur

HOME="/home/builder"

mkdir -p $HOME/.cargo
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
#rustc-wrapper = "sccache"
EOL

chmod 600 $HOME/.gnupg/gpg.conf
#find $HOME/.gnupg -type f -name "*.lock" | xargs rm -f
