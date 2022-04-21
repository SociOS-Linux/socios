#!/bin/bash

echo "Downloading Ubuntu 20.04 unattended installation image."

mkdir -p /tmp/socios

wget -nv --show-progress --load-cookies /tmp/socios/cookies.txt "https://drive.google.com/u/0/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/socios/cookies.txt --keep-session-cookies --no-check-certificate 'https://drive.google.com/u/0/uc?export=download&id=1E0qThUAp9dmbFG9DHLsN5tMgToaebUaL' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1E0qThUAp9dmbFG9DHLsN5tMgToaebUaL" -O /tmp/socios/ubuntu.iso && rm -rf /tmp/socios/cookies.txt

echo "Downloading finished."
