from typing import List, Dict
import json
from argparse import ArgumentParser


def chunk_value(value: str, chunk_size: int, overlap: int) -> List[str]:
    chunks = []
    start = 0
    while start < len(value):
        chunks.append(value[start : (start + chunk_size)])
        start += chunk_size - overlap
    return chunks


def chunk_metadata_value(metada_value, chunk_size, overlap):
    chunks = chunk_value(metada_value["value"], chunk_size, overlap)
    return [
        {
            "chunk": chunks[i],
            "field": metada_value["field"],
            "id": metada_value["id"],
            "index": i,
        }
        for i in range(len(chunks))
    ]


def chunk_metadata_file(file: str, chunk_size: int, overlap: int) -> List[Dict[str, str]]:
    chunked_metadata = []
    with open(file) as f:
        json_data = json.load(f)
        for metadata in json_data:
            chunked_metadata.extend(chunk_metadata_value(metadata, chunk_size, overlap))
    return chunked_metadata


def main(files: List[str], ouput_file: str, chunk_size: int, overlap: int) -> None:
    all_chunked_metadata = []
    for file in files:
        all_chunked_metadata.extend(chunk_metadata_file(file, chunk_size, overlap))
    with open(ouput_file, "w") as f:
        json.dump(all_chunked_metadata, f, indent=4)


if __name__ == "__main__":
    parser = ArgumentParser("prepare_data.py")
    parser.add_argument("input_files", nargs="+", help="List of files to chunk.")
    parser.add_argument("-o", "--output", help="The file to write the output to.")
    parser.add_argument(
        "-c", "--chunk", help="Desired chunk size in characters.", type=int
    )
    parser.add_argument(
        "-ol", "--overlap", help="Chunk overlap in characters.", type=int
    )
    args = parser.parse_args()
    assert args.chunk > args.overlap
    main(args.input_files, args.output, args.chunk, args.overlap)
