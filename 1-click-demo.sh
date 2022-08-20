#!/bin/bash
cd "$(dirname "${BASH_SOURCE[0]}")"
if [ ! -d .venv ]; then
    mkdir .venv
fi

conda create --name lapspython python=3.7
conda activate lapspython
conda install swig pipenv
pipenv sync
pipenv run linting
pipenv run typechecks
pipenv run tests
pipenv run demo
