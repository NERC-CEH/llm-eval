import gc
import json
from argparse import ArgumentParser
from itertools import islice

import torch
from sentence_transformers import SentenceTransformer
from tqdm import tqdm


def batched(iterable, n, *, strict=False):
    if n < 1:
        raise ValueError('n must be at least one')
    iterator = iter(iterable)
    while batch := tuple(islice(iterator, n)):
        if strict and len(batch) != n:
            raise ValueError('batched(): incomplete batch')
        yield batch


def main(input_file: str, output_file: str, model_name: str) -> None:
    model = SentenceTransformer(model_name)
    with open(input_file) as input, open(output_file, "w") as output:
        data = json.load(input)
        batches = list(batched(data, 500))
        position = 0
        for batch in tqdm(batches):
            texts = [chunk["chunk"] for chunk in batch]
            embeddings = model.encode(texts)
            for embedding in embeddings:
                data[position]["embedding"] = embedding.tolist()
                position += 1
            gc.collect()
            torch.cuda.empty_cache()
        json.dump(data, output)


if __name__ == "__main__":
    parser = ArgumentParser("prepare_data.py")
    parser.add_argument("input", help="The file to be used as input.")
    parser.add_argument("output", help="The path to save the processed result.")
    parser.add_argument(
        "-m", "--model", help="Embedding model to use.", default="all-MiniLM-L6-v2"
    )
    args = parser.parse_args()
    main(args.input, args.output, args.model)
