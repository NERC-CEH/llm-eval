import shutil
from argparse import ArgumentParser
from typing import Any, Dict, List, Tuple

import pandas as pd
from haystack import Pipeline
from haystack.components.builders import PromptBuilder
from haystack.components.builders.answer_builder import AnswerBuilder
from haystack_integrations.components.generators.ollama.generator import OllamaGenerator
from haystack_integrations.components.retrievers.chroma import ChromaQueryTextRetriever
from haystack_integrations.document_stores.chroma import ChromaDocumentStore

TMP_DOC_PATH = ".tmp/doc-store"


def build_rag_pipeline(model_name: str, collection_name: str) -> Pipeline:
    document_store = ChromaDocumentStore(
        collection_name=collection_name, persist_path=TMP_DOC_PATH
    )
    retriever = ChromaQueryTextRetriever(document_store, top_k=3)
    print("Creating prompt template...")

    template = """
    Given the following information, answer the question.

    Question: {{query}}

    Context:
    {% for document in documents %}
        {{ document.content }}
    {% endfor %}

    Answer:
    """

    prompt_builder = PromptBuilder(template=template)

    print(f"Setting up model ({model_name})...")
    llm = OllamaGenerator(
        model=model_name,
        generation_kwargs={"num_ctx": 16384},
        url="http://localhost:11434/api/generate",
    )

    answer_builder = AnswerBuilder()

    rag_pipe = Pipeline()

    rag_pipe.add_component("retriever", retriever)
    rag_pipe.add_component("prompt_builder", prompt_builder)
    rag_pipe.add_component("llm", llm)
    rag_pipe.add_component("answer_builder", answer_builder)

    rag_pipe.connect("retriever.documents", "prompt_builder.documents")
    rag_pipe.connect("retriever.documents", "answer_builder.documents")

    rag_pipe.connect("prompt_builder", "llm")

    rag_pipe.connect("llm.replies", "answer_builder.replies")
    return rag_pipe


def run_query(query: str, pipeline: Pipeline) -> Dict[str, Any]:
    return pipeline.run(
        {
            "retriever": {"query": query},
            "prompt_builder": {"query": query},
            "answer_builder": {"query": query},
        }
    )


def query_pipeline(questions: List[str], rag_pipe: Pipeline) -> Tuple[str, List[str]]:
    answers = []
    contexts = []
    for q in questions:
        response = run_query(q, rag_pipe)
        answers.append(response["answer_builder"]["answers"][0].data)
        contexts.append(
            [doc.content for doc in response["answer_builder"]["answers"][0].documents]
        )
    return answers, contexts


def main(
    test_data_file: str,
    ouput_file: str,
    doc_store_path: str,
    collection_name: str,
    model: str,
) -> None:
    shutil.copytree(doc_store_path, TMP_DOC_PATH)

    rag_pipe = build_rag_pipeline(model, collection_name)

    df = pd.read_csv(test_data_file)
    df.drop(columns=["rating", "contexts"], inplace=True)

    answers, contexts = query_pipeline(df["question"], rag_pipe)

    df["answer"] = answers
    df["contexts"] = contexts
    df.to_csv(ouput_file, index=False)

    shutil.rmtree(TMP_DOC_PATH)


if __name__ == "__main__":
    parser = ArgumentParser("run_rag_pipeline.py")
    parser.add_argument(
        "-i",
        "--input",
        help="File containing test queries to generate response from the RAG pipeline.",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="File to output results to.",
    )
    parser.add_argument(
        "-ds",
        "--doc_store",
        help="Path to the doc store.",
    )
    parser.add_argument(
        "-c",
        "--collection",
        help="Collection name in doc store.",
        default="eidc-data",
    )
    parser.add_argument(
        "-m",
        "--model",
        help="Model to use in RAG pipeline.",
        default="llama3.1",
    )
    args = parser.parse_args()
    main(args.input, args.output, args.doc_store, args.collection, args.model)
