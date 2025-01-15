#!/bin/bash
set -e  # 遇到错误立即退出

echo "Ensuring workspace is writable..."
chmod -R a+w /workspace || true

echo "Checking if repository exists..."
if [ ! -d "/workspace/LoginTest" ]; then
    echo "Cloning repository..."
    git clone https://github.com/HuiyuW/LoginTest_Docker.git /workspace/LoginTest
else
    echo "Repository exists. Pulling latest changes..."
    cd /workspace/LoginTest && git pull || echo "Git pull failed, continuing..."
fi

echo "Environment ready. Running interactive shell..."
exec /bin/bash

