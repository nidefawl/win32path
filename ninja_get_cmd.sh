#!/bin/sh
jq -r ".[] | select(.file | contains (\"$@\")) | .command" compile_commands.json