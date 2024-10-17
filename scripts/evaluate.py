from argparse import ArgumentParser
import pandas as pd
from datasets import Dataset
from ragas import evaluate
from ragas.run_config import RunConfig
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.chat_models import ChatOllama
import plotly.graph_objects as go
import plotly.io as pio
import nest_asyncio
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
    context_entity_recall,
    answer_similarity,
    answer_correctness,
)
import json

def main(eval_dataset: str, metric_output: str, image_output: str) -> None:
    nest_asyncio.apply() # apply the event loop async fix
    df = pd.read_csv(eval_dataset, converters={"contexts": pd.eval})
    eval_dataset = Dataset.from_pandas(df)
    llm = ChatOllama(model='mistral-nemo', num_ctx=16384)
    embeddings = OllamaEmbeddings(model='mistral-nemo', num_ctx=16384)
    result = evaluate(
        eval_dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall,
            context_entity_recall,
            answer_similarity,
            answer_correctness,
        ],
        llm=llm,
        embeddings=embeddings,
        raise_exceptions=False,
        run_config=RunConfig(max_workers=1),
    )
    result_df = result.to_pandas()
    pio.templates.default = "gridon"
    fig = go.Figure()

    
    with open(metric_output, "w") as f:
        json.dump(result, f)
    metrics = [metric for metric in result_df.columns.to_list() if metric not in ["question", "ground_truth", "answer", "contexts"]]

    for metric in metrics:
        fig.add_trace(go.Violin(y=result_df[metric], name=metric, points="all", box_visible=True, meanline_visible=True))
    fig.update_yaxes(range=[-0.02,1.02])
    with open(image_output, "wb") as f:
        f.write(fig.to_image(format="png"))



if __name__ == "__main__":
    parser = ArgumentParser("evaluate.py")
    parser.add_argument("eval_dataset", help="File containing the evaluation data.")
    parser.add_argument(
        "-m",
        "--metrics_output",
        help="File to save evaluation metrics to.",
        default="data/metrics.json",
    )
    parser.add_argument(
        "-img",
        "--image_output",
        help="File to save image plot to.",
        default="data/evaluation.png",
    )
    args = parser.parse_args()
    main(args.eval_dataset, args.metrics_output, args.image_output)
