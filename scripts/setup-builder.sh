# Show commands
set -x
# Error
set -e

HOME="/home/builder"

gpg --allow-secret-key-import --import --batch --yes << EOL
$GPG_PRIVATE_KEY
EOL

cat >> $HOME/.gnupg/gpg.conf << EOL
passphrase $GPG_PASSPHRASE
pinentry-mode loopback
no-tty
EOL

chmod 600 $HOME/.gnupg/gpg.conf
#find $HOME/.gnupg -type f -name "*.lock" | xargs rm -f
