#!/bin/bash
args=$(grep -Eo '=(.*)$' in | awk -F= '{print $2}')
python3 tasks/radios.py $args

# dos2unix run.sh