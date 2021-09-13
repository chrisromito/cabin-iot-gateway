#!/usr/bin/env bash
# This script installs all of the system-level deps
# See blog post here: https://lemariva.com/blog/2020/03/tutorial-getting-started-micropython-v20
# Run from the REPO ROOT like:
# $ scripts/install.sh
# #########################

# Variables
export PROJECT_DIR=$(git rev-parse --show-toplevel)
export ESP_DIR="$HOME/esp"
export IDF_PATH="$HOME/esp/esp-idf"
export ESPIDF=$IDF_PATH
mkdir $ESP_DIR
cd $PROJECT_DIR
source scripts/env.sh

echo "Installing tools..."
# Install rust toolchain (required for esptool.py dependencies)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.profile
sudo apt-get install -y wget libncurses-dev flex bison gperf python3 python3-pip python3-setuptools python3-serial python3-click python3-cryptography python3-future python3-pyparsing python3-pyelftools cmake ninja-build ccache libffi-dev libssl-dev python-is-python3
# Download the ESP-IDF framework
cd $ESP_DIR
git clone https://github.com/espressif/esp-idf.git
cd esp-idf
git checkout 4c81978a3e2220674a432a588292a4c860eef27b
git submodule update --init --recursive
## NOTE: the above hash is defined by the variable ESPIDF_SUPHASH_V4 in the file:
# https://github.com/micropython/micropython/blob/master/ports/esp32/Makefile
# Download the ESP-IDF toolchain. This is for the v8.2.0 r2 release compatible with esp-idf v4.0
cd $ESP_DIR
wget https://dl.espressif.com/dl/xtensa-esp32-elf-gcc8_2_0-esp-2019r2-linux-amd64.tar.gz
tar -xzf xtensa-esp32-elf-gcc8_2_0-esp-2019r2-linux-amd64.tar.gz
# Add the crosscompiler to our path
export PATH="$HOME/esp/xtensa-esp32-elf/bin:$PATH"

# Set up app/project-level environment
echo "Tooling setup complete. Setting up application environment..."
cd $PROJECT_DIR
python3 -m venv venv
source venv/bin/activate
pip install esptool
pip install -r requirements.txt
echo "Installation complete"
