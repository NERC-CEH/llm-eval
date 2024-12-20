import json
from argparse import ArgumentParser
from json import JSONDecodeError
from pathlib import Path

import ollama
import pandas as pd
from tqdm import tqdm


def main(input: str, output: str, model: str, prompt_file: str) -> None:
    df = pd.read_csv(input)
    prompt = Path(prompt_file).read_text()
    df["appropriate"] = False
    df["reason"] = ""
    for i, row in tqdm(df.iterrows(), total=len(df)):
        json_q = json.dumps({"question": row["question"], "ground_truth": row["ground_truth"]}, indent=4)
        response = ollama.generate(model=model, prompt=prompt + json_q)
        try:
            result = json.loads(response["response"])
            df.loc[i, "appropriate"] = result["appropriate"]
            df.loc[i, "reason"] = result["reason"]
        except JSONDecodeError:
            df.loc[i, "reason"] = "Error decoding response"
    df.to_csv(output, index=False)


if __name__ == "__main__":
    parser = ArgumentParser("evaluate_synthetic_data.py")
    parser.add_argument("eval_dataset", help="File containing the synthetic questions.")
    parser.add_argument("output", help="File to output the evaluated synthetic data.")
    parser.add_argument("-m", "--model", help="The model to use for evaluation.", default="mistral-nemo")
    parser.add_argument("-p", "--prompt-file", help="File containing the prompt to use for evaluation", default="prompts/synth-eval.txt")
    args = parser.parse_args()
    main(args.eval_dataset, args.output, args.model, args.prompt_file)
