#!/bin/bash
args=$(grep -Eo '=(.*)$' in | awk -F= '{print $2}')
python3 gen.py $args