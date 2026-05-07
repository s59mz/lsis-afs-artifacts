#!/bin/bash

set -e

# python3 -m pip install -e .[dev]

pytest -v  tests/ -m "not slow"
