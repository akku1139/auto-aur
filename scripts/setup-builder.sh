# Show commands
set -x
# Error
set -e

HOME="/home/builder"

mkdir -p $HOME/.cargo $HOME/.ccache

gpg --allow-secret-key-import --import --batch --yes << EOL
$GPG_PRIVATE_KEY
EOL

cat >> $HOME/.gnupg/gpg.conf << EOL
passphrase $GPG_PASSPHRASE
pinentry-mode loopback
no-tty
EOL

cat > $HOME/.ccache/ccache.conf << EOL

EOL

cat > $HOME/.cargo/config << EOL
[build]
rustc-wrapper = "sccache"
EOL

chmod 600 $HOME/.gnupg/gpg.conf
#find $HOME/.gnupg -type f -name "*.lock" | xargs rm -f
