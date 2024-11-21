#!/bin/bash
dvc queue remove --all
dvc exp run --queue -S hp.chunk-size=400 -S sub-sample=1 -S max-length=500
dvc exp run --queue -S hp.chunk-size=600 -S sub-sample=1 -S max-length=500
dvc queue start
dvc queue status
echo "Run `dvc queue status` to check the state of the experiments"
