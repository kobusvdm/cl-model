#!/bin/sh

. $_SRC_DIR/dev-env/99.env.sh

asdf plugin add poetry
asdf install poetry $POETRY_VER
asdf local poetry $POETRY_VER

asdf plugin add python
asdf install python $PYTHON_VER
asdf local python $PYTHON_VER

asdf plugin add azure-cli
asdf install azure-cli $AZURE_VER
asdf local azure-cli $AZURE_VER

if ! command -v arkade &> /dev/null; then
    mkdir $_TMP_DIR
    #0
    _pushd $_TMP_DIR #1
    curl -sLS https://get.arkade.dev | sh
    mkdir -p ~/.local/bin
    cp arkade ~/.local/bin
    _popd #0
fi

poetry lock && poetry install
poetry config virtualenvs.in-project true