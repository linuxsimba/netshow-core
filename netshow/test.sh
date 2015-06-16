#!/bin/bash

# Testing Script for netshow-core

# Switch to the correct directory
if [ ! -f setup.py ]; then
  cd `dirname $0`
fi

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

# Go into the temp directory and install netshow-lib
echo "Go into temp install directory"
cd .temp
echo " Install netshow-core-lib"
git clone ssh://git@github.com/CumulusNetworks/netshow-core.git netshow-core
cd netshow-core/netshow-lib

echo "Move into devel branch"
git checkout devel

echo "Create wheel for netshow-core-lib"
python setup.py bdist_wheel
echo "Install wheel in wheel directory"
cp dist/* ../../../wheel_dir/

# run tox
echo "Run tox"
cd ../../../
tox

