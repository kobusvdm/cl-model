#!/bin/sh

. $_SRC_DIR/dev-env/99.env.sh

REPOSRC=https://github.com/asdf-vm/asdf.git
LOCALREPO=~/.asdf

if ! command -v asdf &> /dev/null; then
  [ -d $LOCALREPO ] && echo "asdf not found but repo folder already present" && ((exit 1 2>/dev/null) || return 1)
  [ -d $LOCALREPO ] || git clone $REPOSRC $LOCALREPO

  (_pushd "$LOCALREPO" && git pull --rebase origin master && _popd)

  git clone $REPOSRC $LOCALREPO --branch $ASDF_REPO_VER
else
  echo "asdf already installed"
  echo "Updating asdf"
  (_pushd "$LOCALREPO" && git pull --rebase origin master && _popd)
fi

