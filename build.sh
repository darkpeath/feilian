#!/usr/bin/env bash

python -m pip install pip
python -m pip install --upgrade build wheel
python -m pip install -r requirements.txt
python -m build
