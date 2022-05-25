#!/bin/bash

cd ~

if [ -d socios/image ]; then
        echo "Desitination available"
		
else
 
mkdir -p socios/image

fi

echo "Checking For Fedora  ISO Images in Destination."

if find ~/socios/image -name Fedora.iso | grep -q 'Fedora'; then
 
echo "Fedora ISO Image Available in Destination. Choose your partition Space."

else

echo "Downloading Fedora ISO Image file in Destination"

wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=14SVzPnIi7qw9s5NwjvJYztdqo0L_lFuH' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=14SVzPnIi7qw9s5NwjvJYztdqo0L_lFuH" -O /tmp/Fedora.iso

echo "Copying the ISO image file to Socios Destination"

cp /tmp/socios/Fedora.iso ~/socios/image/

rm -rf /tmp/cookies.txt

echo "Downloading finished."

fi
