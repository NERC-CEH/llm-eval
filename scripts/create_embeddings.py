import json
from argparse import ArgumentParser

from sentence_transformers import SentenceTransformer
from torch import Tensor
from tqdm import tqdm


def create_embedding(text: str) -> Tensor:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return model.encode(text)


def main(input_file: str, output_file: str) -> None:
    with open(input_file) as input, open(output_file, "w") as output:
        data = json.load(input)
        for chunk in tqdm(data):
            chunk["embedding"] = create_embedding(chunk["chunk"]).tolist()
        json.dump(data, output)


if __name__ == "__main__":
    parser = ArgumentParser("prepare_data.py")
    parser.add_argument("input", help="The file to be used as input.")
    parser.add_argument("output", help="The path to save the processed result.")
    args = parser.parse_args()
    main(args.input, args.output)
