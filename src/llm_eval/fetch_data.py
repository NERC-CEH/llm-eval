import json


def main():
    data = {
        "datasets": [
            {"name": "dsone", "desc": "some description"},
            {"name": "dstwo", "desc": "some text"},
        ]
    }
    with open("data/eidc_metadata.json", "w") as f:
        json.dump(data, f)


if __name__ == "__main__":
    main()
