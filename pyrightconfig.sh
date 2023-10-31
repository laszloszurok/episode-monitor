#!/bin/sh

if [ -z "$(command -v hatch)" ]; then
    echo "hatch is not installed"
    exit 1
fi

if ! [ -f pyrightconfig.json ]; then
    echo "generating pyrightconfig.json"
    venv="$(hatch env find)"
    venv_path="$(dirname "$venv")"
    venv_name="$(basename "$venv")"
    printf "%s\n  %s\n  %s\n  %s\n%s\n" \
        "{" "\"venvPath\": \"$venv_path\"," "\"venv\": \"$venv_name\"," "\"executionEnvironments\": [{\"root\": \"src/$venv_name\"}]" "}" \
        > pyrightconfig.json
else
    echo "pyrightconfig.json exists already"
fi
