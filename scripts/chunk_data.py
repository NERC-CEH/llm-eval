import json
from argparse import ArgumentParser
from typing import Any, Dict, List


def chunk_value(value: str, chunk_size: int, overlap: int, max_length: int) -> List[str]:
    chunks = []
    start = 0
    end = max_length if len(value) > max_length > 0 else len(value)
    while start < end:
        chunks.append(value[start : (start + chunk_size)])
        start += chunk_size - overlap
    return chunks


def chunk_metadata_value(
    metada_value: str, chunk_size: int, overlap: int, max_length: int
) -> List[Dict[str, Any]]:
    chunks = chunk_value(metada_value["value"], chunk_size, overlap, max_length)
    return [
        {
            "chunk": chunks[i],
            "field": metada_value["field"],
            "id": metada_value["id"],
            "index": i,
        }
        for i in range(len(chunks))
    ]


def chunk_metadata_file(
    file: str, chunk_size: int, overlap: int, max_length: int
) -> List[Dict[str, str]]:
    chunked_metadata = []
    with open(file) as f:
        json_data = json.load(f)
        for metadata in json_data:
            chunked_metadata.extend(chunk_metadata_value(metadata, chunk_size, overlap, max_length))
    return chunked_metadata


def main(files: List[str], ouput_file: str, chunk_size: int, overlap: int, max_length: int) -> None:
    all_chunked_metadata = []
    for file in files:
        all_chunked_metadata.extend(chunk_metadata_file(file, chunk_size, overlap, max_length))
    with open(ouput_file, "w") as f:
        json.dump(all_chunked_metadata, f, indent=4)


if __name__ == "__main__":
    parser = ArgumentParser("prepare_data.py")
    parser.add_argument("input_files", nargs="+", help="List of files to chunk.")
    parser.add_argument(
        "-o",
        "--output",
        help="The json file to write the output to.",
        type=str,
        nargs="?",
        const="chunk_data_output.json",
    )
    parser.add_argument(
        "-c",
        "--chunk",
        help="Desired chunk size in characters.",
        type=int,
        nargs="?",
        const=300,
    )
    parser.add_argument(
        "-ol",
        "--overlap",
        help="Chunk overlap in characters.",
        type=int,
        nargs="?",
        const=100,
    )
    parser.add_argument(
        "-m",
        "--max_length",
        help="""Maximum length of data in characters - meant for truncating large 
        strings in testing. 0 defaults to all data""",
        type=int,
        nargs="?",
        const=0,
    )
    args = parser.parse_args()
    assert args.chunk > args.overlap
    main(args.input_files, args.output, args.chunk, args.overlap, args.max_length)
