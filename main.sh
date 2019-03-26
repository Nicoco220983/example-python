#!/bin/bash
HERE=$(dirname $0)
export PYTHONPATH="$HERE/src:$PYTHONPATH"
"$HERE"/src/LogMonitorer.py "$@"
