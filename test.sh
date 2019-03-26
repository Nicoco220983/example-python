#!/bin/bash
HERE=$(dirname $0)
export PYTHONPATH="$HERE/src:$PYTHONPATH"
python3 -m unittest discover -v "$HERE/test" "*_test.py"
