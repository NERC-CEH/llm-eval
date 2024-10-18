import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

metrics = {
    "answer_relevancy",
    "answer_correctness",
    "context_precision",
    "context_recall",
}
dummy_data = {metric: np.random.rand(100) for metric in metrics}
df = pd.DataFrame(dummy_data)

with open("metrics.txt", "w") as f:
    for col in df:
        f.write(f"{col}: {df[col].mean()}\n")

pio.templates.default = "gridon"
fig = go.Figure()
metrics = [
    metric
    for metric in df.columns.to_list()
    if metric not in ["question", "ground_truth", "answer", "contexts"]
]
for metric in metrics:
    fig.add_trace(
        go.Violin(
            y=df[metric],
            name=metric,
            points="all",
            box_visible=True,
            meanline_visible=True,
        )
    )
fig.update_yaxes(range=[-0.02, 1.02])
fig.write_image("metrics.png")
