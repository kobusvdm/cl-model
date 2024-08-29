#!/bin/sh

if [ -z "${_SRC_DIR}" ]; then
    _SRC_DIR=$(realpath $(pwd))
fi

. $_SRC_DIR/versions.sh

_pushd () {
    "$(command -v pushd)" "$@" > /dev/null
}

_popd () {
    "$(command -v popd)" > /dev/null
}

# Variables
# Base vars
_TMP_DIR="${_SRC_DIR}/.temp"
_BIN_DIR="${_TMP_DIR}/bin"
_STATE_DIR="${_TMP_DIR}/state"

case ":$_BIN_DIR:" in
    *":${PATH}:"*) ;;
    *) export PATH="${_BIN_DIR}:${PATH}" ;;
esac

PREFECT_HOME="${_SRC_DIR}/.prefect"
PREFECT_LOGGING_ROOT_LEVEL=INFO
[ -z "$(echo $PATH | grep $HOME/.asdf/bin)" ] && export PATH=$PATH:$HOME/.asdf/bin:$HOME/.asdf/shims
ASDF_DIR=$HOME/.asdf

AZ_RESOURCE_GROUP=rg-pl42
AZ_LOCATION=westeurope
AZ_STORAGE_ACCOUNT=pl42storage
# End vars

export _pushd _popd

#Variable exports
export _SRC_DIR _TMP_DIR _BIN_DIR _STATE_DIR PREFECT_HOME ASDF_DIR PREFECT_LOGGING_ROOT_LEVEL AZ_RESOURCE_GROUP AZ_LOCATION AZ_STORAGE_ACCOUNT

    