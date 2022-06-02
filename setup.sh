#!/bin/bash
MYPATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $MYPATH
mkdir images
python3 -m venv ./myvenv
source ./myvenv/bin/activate
pip3 install -r requirements.txt
deactivate

