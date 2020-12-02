#!/usr/bin/bash

# Note, assumes you have manually installed black and flake8
python3 -m black day*/*.py
python3 -m flake8 day*/*.py
