#!/bin/bash
cd "$(dirname "${BASH_SOURCE[0]}")"
conda create --name lapspython python=3.7
conda activate lapspython
conda install swig asdf pipenv
pipenv install --dev
pipenv run linting
pipenv run typechecks
pipenv run tests
pipenv run demo
