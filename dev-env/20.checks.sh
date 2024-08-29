#!/bin/sh

. $_SRC_DIR/dev-env/99.env.sh
  
if ! command -v asdf &> /dev/null; then
  echo "Failed to install or find asdf"
fi

