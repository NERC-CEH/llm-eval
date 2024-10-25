import json
from argparse import ArgumentParser
from typing import Dict, List

METADATA_FIELDS = ["title", "description", "lineage"]


def extact_eidc_metadata_fields(
    json_data: Dict, fields: List[str] = METADATA_FIELDS
) -> List[Dict[str, str]]:
    metadatas = []
    for field in fields:
        if json_data[field]:
            metadata = {}
            metadata["id"] = json_data["identifier"]
            metadata["field"] = field
            metadata["value"] = json_data[field]
            metadatas.append(metadata)
    return metadatas


def parse_eidc_metadata(file_path: str) -> List[Dict[str, str]]:
    data = []
    with open(file_path) as f:
        json_data = json.load(f)
        for dataset in json_data["results"]:
            dataset_metadata = extact_eidc_metadata_fields(dataset)
            data.extend(dataset_metadata)
    return data


def main(input: str, output: str) -> None:
    data = parse_eidc_metadata(input)
    with open(output, "w") as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    parser = ArgumentParser("prepare_data.py")
    parser.add_argument("input", help="The file to be used as input.")
    parser.add_argument("output", help="The path to save the processed result.")
    args = parser.parse_args()
    main(args.input, args.output)
