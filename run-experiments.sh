#!/bin/bash
NC='\033[0m'
GREEN='\033[0;32m'
dvc queue remove --all
models=("llama3 llama3.1 mistral-nemo")
for model in $models
do
    dvc exp run --queue -S rag.model=$model
done
dvc queue start
dvc queue status
echo -e "Run ${GREEN}dvc queue status${NC} to check the state of the experiments"
