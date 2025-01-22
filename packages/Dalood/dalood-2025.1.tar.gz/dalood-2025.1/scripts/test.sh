#!/usr/bin/env bash
set -euo pipefail

SELF=$(readlink -f "${BASH_SOURCE[0]}")
DIR=${SELF%/*/*}

cd -- "$DIR"
./scripts/install_in_venv.sh test
source ./venv/bin/activate
python -m coverage run -m unittest discover -v ./test
python -m coverage "${1:-report}"
