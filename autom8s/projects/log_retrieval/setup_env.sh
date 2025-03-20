#!/bin/bash

usage() {
    echo "Usage: $0 "
    echo "[-e|--env] {'' | dev}"
    echo "   An optional environment. Specify 'dev' if you plan on commit changes to the project"
    echo "[-h|--help]"
    echo "   Display this help message"
    exit 1
}

ENVIRONMENT=""
install_precommit=false

while [ "$1" != "" ]; do
    case $1 in
    -e | --env)
        shift # remove `-e` or `--env` from `$1`
        ENVIRONMENT=$1
        ;;
    -h | --help)
        usage # run usage function
        ;;
    *)
        usage
        exit 1
        ;;
    esac
    shift # remove the current value for `$1` and use the next
done

env_options=("" "dev")

if [ "$ENVIRONMENT" == "" ]; then
    suffix=""
elif [ "$ENVIRONMENT" == "dev" ]; then
    suffix="-dev"
    install_precommit=true
else
    echo "Invalid environment: $ENVIRONMENT"
    exit 1
fi

python3.13 -m venv .venv
source .venv/bin/activate

pip install -r requirements${suffix}.txt

if [ "$install_precommit" == "true" ]; then
    pre-commit install
fi
