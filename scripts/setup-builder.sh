# Show commands
set -x
# Error
set -e

sudo -u builder gpg --allow-secret-key-import --import --batch --yes << EOL
$GPG_PRIVATE_KEY
EOL

cat >> ~/.gnupg/gpg.conf << EOL
passphrase $GPG_PASSPHRASE
pinentry-mode loopback
no-tty
EOL

chmod 600 ~/.gnupg/gpg.conf
#chown -R builder:builder $HOME/.gnupg
#find /.gnupg -type f | xargs ls -l
#find $HOME/.gnupg -type f -name "*.lock" | xargs rm -f
