#!/bin/bash

echo "Downloading Ubuntu 20.04 unattended installation image."

mkdir -p /tmp/socios

wget -nv --show-progress --load-cookies /tmp/socios/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/socios/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1ZiqnQn_Ddp1-SQQvqbA2eequ2te6hV2N' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1ZiqnQn_Ddp1-SQQvqbA2eequ2te6hV2N" -O /tmp/socios/ubuntu.iso && rm -rf /tmp/socios/cookies.txt

echo "Downloading finished."
