import json
import os
import shutil
import sys
import uuid
from argparse import ArgumentParser
import logging

__import__("pysqlite3")
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
import chromadb
from chromadb.utils import embedding_functions
from chromadb.utils.batch_utils import create_batches

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

def main(
    input_file: str, output_path: str, collection_name: str, embedding_model: str
) -> None:
    logger.info(f"Uploading data ({input_file}) to chromaDB ({output_path}) in collection {collection_name}.")
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
        
        batches = create_batches(
            api=client, ids=ids, documents=docs, embeddings=embs, metadatas=metas
        )
        logger.info(f"Uploading {len(docs)} document(s) to chroma in {len(batches)} batch(es).")
        for batch in batches:
            collection.add(
                documents=batch[3],
                metadatas=batch[2],
                embeddings=batch[1],
                ids=batch[0],
            )
        docs_in_col = collection.count()
        logger.info(f"{docs_in_col} documents(s) are now in the {collection_name} collection")


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
