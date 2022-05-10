#!/bin/bash

echo "Checking For Ubuntu ISO Images in Destination."

find /tmp/socios -name ubuntu.iso

if find /tmp/socios -name ubuntu.iso | grep -q 'ubuntu'; then
 
echo "Ubuntu ISO Image Available in Destination. Choose your partition Space."

else

echo "Downloading Ubuntu ISO Image file in Destination"

mkdir -p /tmp/socios

wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1E0qThUAp9dmbFG9DHLsN5tMgToaebUaL' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1E0qThUAp9dmbFG9DHLsN5tMgToaebUaL" -O /tmp/socios/ubuntu.iso

rm -rf /tmp/cookies.txt

echo "Downloading finished."

fi