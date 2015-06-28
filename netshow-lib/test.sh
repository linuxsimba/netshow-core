#!/bin/bash

if [ ! -d setup.py ]; then
  cd `dirname $0`
fi

set -e

echo "starting up"

git clean -xdf

PATH=$WORKSPACE/venv/bin:/usr/local/bin:$PATH
if [ ! -d "venv" ]; then
        virtualenv venv
fi
. venv/bin/activate

pip install --upgrade -r requirements_develop.txt
tox
