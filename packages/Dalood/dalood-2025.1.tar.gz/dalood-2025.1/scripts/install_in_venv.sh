#!/usr/bin/env bash
set -euo pipefail

SELF=$(readlink -f "${BASH_SOURCE[0]}")
DIR=${SELF%/*/*}

if [[ -n ${1:-} ]]
then
  optdep="[$1]"
else
  optdep=""
fi

cd -- "$DIR"
python3 -m venv ./venv
source ./venv/bin/activate
pip install -U pip
pip install -U -e ".$optdep"
