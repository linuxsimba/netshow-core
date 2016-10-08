#!/bin/bash

# Testing Script for netshow-core


# Switch to the correct directory
if [ ! -f setup.py ]; then
  cd `dirname $0`
fi

echo "clean out the whole repo"
cd ../
git clean -xdf
cd netshow

set -e

echo "starting up"
PATH=$WORKSPACE/venv/bin:/usr/local/bin:$PATH
if [ ! -d "venv" ]; then
        virtualenv venv
fi
. venv/bin/activate

# install test requirements like tox
pip install --upgrade -r requirements_develop.txt

# Delete working directories
if [ -d wheel_dir ]; then
  echo "Delete wheel directory"
  rm -rf wheel_dir
fi
if [ -d .temp ]; then
  echo "Delete temp install directory"
  rm -rf .temp
fi

# Make working directories
echo "Create wheel directory"
mkdir wheel_dir
echo "Create temp install directory"
mkdir .temp

echo "Go into the netshow-core netshow-lib directory"
cd ../netshow-lib

echo "Create wheel for netshow-core-lib"
python setup.py bdist_wheel
echo "Install wheel in wheel directory"
cp dist/* ../netshow/wheel_dir/

# run tox
echo "Run tox in the netshow directory"
cd ../netshow/
tox
