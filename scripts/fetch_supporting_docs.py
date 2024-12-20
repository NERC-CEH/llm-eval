import json
import logging
import os
from argparse import ArgumentParser
from typing import Dict, List

import requests
from dotenv import load_dotenv
from tqdm import tqdm

logger = logging.getLogger(__name__)


def extract_ids_and_titles(metadata_file: str) -> List[str]:
    with open(metadata_file) as f:
        json_data = json.load(f)
        titles = [dataset["title"] for dataset in json_data["results"]]
        ids = [dataset["identifier"] for dataset in json_data["results"]]
        return list(zip(titles, ids))


def get_supporting_docs(datset_title: str, eidc_id: str, user: str, password: str) -> List[Dict[str, str]]:
    try:
        res = requests.get(
            f"https://legilo.eds-infra.ceh.ac.uk/{eidc_id}/documents",
            auth=(user, password),
        )
        json_data = res.json()
        docs = []
        for key, val in json_data["success"].items():
            docs.append({"dataset": datset_title, "id": eidc_id, "field": key, "value": val})
        return docs
    except Exception as e:
        logger.error(
            f"Failed to download supporting docs for dataset {eidc_id}", exc_info=e
        )
        return []


def main(metadata_file: str, supporting_docs_file: str) -> None:
    load_dotenv()
    user = os.getenv("username")
    password = os.getenv("password")
    ids_and_titles = extract_ids_and_titles(metadata_file)
    docs = []
    for id_title in tqdm(ids_and_titles):
        docs.extend(get_supporting_docs(id_title[0], id_title[1], user, password))
    with open(supporting_docs_file, "w") as f:
        json.dump(docs, f, indent=4)


if __name__ == "__main__":
    parser = ArgumentParser("fetch_supporting_docs.py")
    parser.add_argument("metadata", help="File containing EIDC metadata.")
    parser.add_argument("supporting_docs", help="File to save supporting docs to.")
    args = parser.parse_args()
    main(args.metadata, args.supporting_docs)
