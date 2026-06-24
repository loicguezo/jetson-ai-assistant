#!/usr/bin/env bash

set -e

# To make sure you have the latest mirrors available
sudo apt update -y

packages=("v4l2loopback-dkms" "python3")

for p in "${packages[@]}"; do
    if ! dpkg -s "$p" >/dev/null 2>&1; then
        echo "Installation of $p..."
        sudo apt install -y "$p"
    else
        echo "$p already installed."
    fi
done
