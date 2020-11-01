#!/usr/bin/env bash

python3 setup.py sdist bdist_wheel
python3 -m pip uninstall csv-split -y
python3 setup.py install