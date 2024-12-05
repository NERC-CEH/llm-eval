import json
import logging
from argparse import ArgumentParser
from typing import List

from langchain.docstore.document import Document
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
from ragas.run_config import RunConfig
from ragas.testset.evolutions import multi_context, reasoning, simple
from ragas.testset.generator import TestsetGenerator

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.StreamHandler()],
)


def load_metadata(metadata_file: str) -> List[Document]:
    with open(metadata_file) as f:
        json_data = json.load(f)
        return [
            Document(
                page_content=metadata["value"],
                metadata={"id": metadata["id"], "field": metadata["field"]},
            )
            for metadata in json_data
        ]


def main(metadata_file: str, testset_output_file: str, testset_size: int = 5) -> None:
    docs = load_metadata(metadata_file)
    logger.info(f"Loaded {len(docs)} documents from {metadata_file}")
    llm = ChatOllama(model="mistral-nemo", num_ctx=16384)
    embeddings = OllamaEmbeddings(model="mistral-nemo", num_ctx=16384)
    gen = TestsetGenerator.from_langchain(
        llm, llm, embeddings, run_config=RunConfig(max_workers=1, max_retries=2)
    )
    dist = {simple: 0.6, multi_context: 0.2, reasoning: 0.2}
    testset = gen.generate_with_langchain_docs(docs, testset_size, dist)
    df = testset.to_pandas()
    df.to_csv(testset_output_file, index=False)


if __name__ == "__main__":
    parser = ArgumentParser("generate_synthetic_testset.py")
    parser.add_argument(
        "metadata_file",
        help="Input file containing metadata to base the synthetic test questions on.",
    )
    parser.add_argument(
        "testset_file",
        help="Output file to write the test set to.",
    )
    parser.add_argument(
        "testset_size",
        help="How many questions to generate in the test set.",
        type=int,
        nargs="?",
        const=5,
    )
    args = parser.parse_args()
    main(args.metadata_file, args.testset_file, args.testset_size)
