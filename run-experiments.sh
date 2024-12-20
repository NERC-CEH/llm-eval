#!/bin/bash
NC='\033[0m'
GREEN='\033[0;32m'
uv run dvc queue remove --all
models=("llama3 llama3.1 mistral-nemo")
for model in $models
do
    uv run dvc exp run --queue -S rag.model=$model -S sub-sample=1 -S max-length=250 -S test-set-size=5
done
uv run dvc queue start
uv run dvc queue status
echo -e "Use ${GREEN}uv run dvc queue status${NC} to check the state of the experiments"
