#!/bin/sh

. $_SRC_DIR/dev-env/99.env.sh

echo $_SRC_DIR

poetry run prefect config set PREFECT_RESULTS_PERSIST_BY_DEFAULT=true
poetry run prefect server start
poetry run prefect block register --file src/StorageApi.py
