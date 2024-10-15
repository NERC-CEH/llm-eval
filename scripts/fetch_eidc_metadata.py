import requests
import json
from argparse import ArgumentParser

URL = "https://catalogue.ceh.ac.uk/eidc/documents"

def main(output_file: str) -> None:
    res = requests.get(
        URL,
        headers={"content-type": "application/json"},
        params={
            "page": 1,
            "rows": 2500,
            "term": "recordType:Dataset",
        },
    )
    with open(output_file, "w") as f:
        json.dump(res.json(), f, indent=4)


if __name__ == "__main__":
    parser = ArgumentParser("fetch_eidc_metadata.py")
    parser.add_argument("output", help="The file path to save the downloaded data to.")
    args = parser.parse_args()
    main(args.output)
