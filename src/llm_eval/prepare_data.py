import json
from sentence_transformers import SentenceTransformer

def create_embedding(text):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return model.encode(text) 


def main():
    with open("data/eidc_metadata.json") as input, open("data/prepared_data.json", "w") as output:
        data = json.load(input)
        for dataset in data["datasets"]:
            dataset["desc_emb"] = create_embedding(dataset["desc"]).tolist()
        json.dump(data, output)


if __name__ == "__main__":
    main()
