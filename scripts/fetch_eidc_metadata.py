import json
from argparse import ArgumentParser

import requests

URL = "https://catalogue.ceh.ac.uk/eidc/documents"


def main(output_file: str, sample: int) -> None:
    res = requests.get(
        URL,
        headers={"content-type": "application/json"},
        params={
            "page": 1,
            "rows": 2500,
            "term": "recordType:Dataset",
        },
    )
    json_data = res.json()
    json_data["results"] = json_data["results"][:sample]
    with open(output_file, "w") as f:
        json.dump(json_data, f, indent=4)


if __name__ == "__main__":
    parser = ArgumentParser("fetch_eidc_metadata.py")
    parser.add_argument("output", help="The file path to save the downloaded data to.")
    parser.add_argument(
        "-s",
        "--sample",
        help="Only save n datasets",
        type=int,
        nargs="?",
        const=0,
    )
    args = parser.parse_args()
    main(args.output, args.sample)
