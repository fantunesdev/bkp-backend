#!/bin/bash

cd /var/lib/bkp-backend/
source .venv/bin/activate

python backup/main.py $1
