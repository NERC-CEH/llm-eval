#!/bin/bash

echo "Setting up dvc test run..."

uv run dvc exp run -S sub-sample=1 -S max-length=250 -S test-set-size=5 -n test-run -f
