#!/bin/sh

if [ -z "$(command -v hatch)" ]; then
    echo "hatch is not installed"
    exit 1
fi

if ! [ -f pyrightconfig.json ]; then
    echo "generating pyrightconfig.json"
    venv_path="$(hatch env find)"
    venv_name="$(basename "$venv_path")"
    echo "{ \"venvPath\": \"$venv_path\", \"venv\": \"$venv_name\"}" > pyrightconfig.json
else
    echo "pyrightconfig.json exists already"
fi
