#!/bin/sh

. $_SRC_DIR/dev-env/99.env.sh

echo $_SRC_DIR

poetry run prefect server stop
