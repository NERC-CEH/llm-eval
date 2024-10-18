from argparse import ArgumentParser
import logging
import json
from tqdm import tqdm
import requests
import os
from typing import Dict, List
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

def extract_ids(metadata_file: str):
    with open(metadata_file) as f:
        json_data = json.load(f)
        ids = [dataset["identifier"] for dataset in json_data["results"]]
        return ids


def get_supporting_docs(eidc_id: str, user: str, password: str) -> List[Dict[str, str]]:
    try:
        res = requests.get(
            f"https://legilo.eds-infra.ceh.ac.uk/{eidc_id}/documents", auth=(user, password)
        )
        json_data = res.json()
        docs = []
        for key, val in json_data["success"].items():
            docs.append({"id": eidc_id, "field": key, "value": val})
        return docs
    except Exception as e:
        logger.error(f"Failed to download supporting docs for dataset {eidc_id}", exc_info=e)
        return []


def main(metadata_file: str, supporting_docs_file: str):
    load_dotenv()
    user = os.getenv("username")
    password = os.getenv("password")
    ids = extract_ids(metadata_file)
    docs = []
    for id in tqdm(ids):
        docs.extend(get_supporting_docs(id, user, password))
    with open(supporting_docs_file, "w") as f:
        json.dump(docs, f, indent=4)


if __name__ == "__main__":
    parser = ArgumentParser("fetch_supporting_docs.py")
    parser.add_argument("metadata", help="File containing EIDC metadata.")
    parser.add_argument("supporting_docs", help="File to save supporting docs to.")
    args = parser.parse_args()
    main(args.metadata, args.supporting_docs)
