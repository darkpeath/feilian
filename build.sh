#!/usr/bin/env bash

<<<<<<< HEAD
python -m pip install --upgrade pip
python -m pip install --upgrade build wheel
=======
python -m pip install pip
python -m pip install --upgrade build wheel
python -m pip install -r requirements.txt
>>>>>>> 2c9fb3bff11a8472a9c5067e915056ed265e72fc
python -m build
