#!/bin/bash

cd netshow-lib

set -e

echo "starting up"

PATH=$WORKSPACE/venv/bin:/usr/local/bin:$PATH
if [ ! -d "venv" ]; then
        virtualenv venv
fi
. venv/bin/activate

pip install --upgrade -r requirements_develop.txt
tox
