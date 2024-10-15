from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser("prepare_data.py")
    parser.add_argument("input_file", nargs="+", help="File containing chunks and embeddings to upload to document store")
    parser.add_argument("-o", "--output", help="The file to write the output to.")