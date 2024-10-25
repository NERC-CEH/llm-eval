import json
import os
import shutil
import uuid
from argparse import ArgumentParser

import chromadb
from chromadb.utils import embedding_functions


def main(
    input_file: str, output_path: str, collection_name: str, embedding_model: str
) -> None:
    if os.path.exists(output_path):
        shutil.rmtree(output_path)

    with open(input_file) as f:
        json_data = json.load(f)

        docs = [chunk["chunk"] for chunk in json_data]
        metas = [
            {field: chunk[field] for field in ["field", "id", "index"]}
            for chunk in json_data
        ]
        embs = [chunk["embedding"] for chunk in json_data]
        ids = [uuid.uuid4().hex for _ in json_data]

        func = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=embedding_model
        )

        client = chromadb.PersistentClient(output_path)
        collection = client.create_collection(
            name=collection_name, embedding_function=func
        )
        collection.add(documents=docs, metadatas=metas, embeddings=embs, ids=ids)


if __name__ == "__main__":
    parser = ArgumentParser("prepare_data.py")
    parser.add_argument(
        "input_file",
        help="File containing chunks and embeddings to upload to document store",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="The file to write the output to.",
        default="data/chroma-data",
    )
    parser.add_argument(
        "-c",
        "--collection",
        help="Collection name to use in doc store.",
        default="eidc-data",
    )
    parser.add_argument(
        "-em",
        "--embedding_model",
        help="""Embedding model to use in the doc store (must be the same as the
        function used to create embeddings.)""",
        default="all-MiniLM-L6-v2",
    )
    args = parser.parse_args()
    main(args.input_file, args.output, args.collection, args.embedding_model)
