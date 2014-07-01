#!/bin/bash
cd $(dirname $0)
cd src
python quail.py go
stty echo
