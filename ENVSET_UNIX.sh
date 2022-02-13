#!/bin/sh
# For use in cygwin/git bash
# Use with: source ENVSET_UNIX.sh
# WIP, fucks up $PATH and doesn't work on zsh
if [ ! "x${ZSH_VERSION}" = "x" ]; then
BASH_SOURCE=${(%):-%x}
fi
BASEDIR=$(dirname "$BASH_SOURCE")
SECTION=${1:-CLANG}
IFS=$'\r\n'
for ENV_SETTING in `python "${BASEDIR}/ENV_readini.py" -t u $SECTION`;
do 
    NAME=${ENV_SETTING%=*}
    VAL=${ENV_SETTING#*=}
    printf -v "${NAME}" "%s" "${VAL}"
    export ${NAME}
done