from argparse import ArgumentParser
from haystack import Pipeline
from haystack_integrations.document_stores.chroma import ChromaDocumentStore
from haystack_integrations.components.retrievers.chroma import ChromaQueryTextRetriever
from haystack.components.builders import PromptBuilder
from haystack_integrations.components.generators.ollama.generator import OllamaGenerator
from haystack.components.builders.answer_builder import AnswerBuilder
import pandas as pd


def build_rag_pipeline(model_name: str) -> Pipeline:
    document_store = ChromaDocumentStore(
        collection_name="eidc-data", persist_path="data/chroma-data"
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

    model_name = "llama3.1"

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


def query_pipeline(query: str, pipeline: Pipeline):
    return pipeline.run(
        {
            "retriever": {"query": query},
            "prompt_builder": {"query": query},
            "answer_builder": {"query": query},
        }
    )


def main(test_data_file: str):
    rag_pipe = build_rag_pipeline("llama3.1")

    df = pd.read_csv(test_data_file)
    responses = []
    for q in df["question"]:
        responses.append(query_pipeline(q, rag_pipe))
    df["rag_response"] = responses
    df.to_csv("data/rag_response.csv")

    query = "Who collected the land cover map data?"
    result = rag_pipe.run(
        {
            "retriever": {"query": query},
            "prompt_builder": {"query": query},
            "answer_builder": {"query": query},
        }
    )
    print(result)


if __name__ == "__main__":
    parser = ArgumentParser("run_rag_pipeline.py")
    parser.add_argument(
        "test_data_file",
        help="File containing test queries to generate response from the RAG pipeline.",
    )
    args = parser.parse_args()
    main(args.test_data_file)
