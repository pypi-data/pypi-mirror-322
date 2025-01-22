import argparse
import json
import os
from pathlib import Path
import glob

from ..logic import get_all_kmers
from ...core import utils


def gather_output(input_data_dir: str, out_file_dir: str):
    """
    Post-processing of sequence-pair hadamard products, we need to gather all of them and find the list of conserved
    k-mers within the sequences

    :param(str) input_data_dir: Absolute path to folder where all the hadamard matrices are saved
    :param(str) out_file_dir: Folder path to write result
    """
    print(
        f"Reading hadamard products from {input_data_dir} to find conserved k-mers"
    )
    Path(out_file_dir).mkdir(parents=True, exist_ok=True)
    hadamard_matrices = []  # List of hadamard matrices
    sequences = []
    k = None
    input_data_dir = Path(input_data_dir)
    files = glob.glob(input_data_dir.as_posix() + "/output_*.json")
    fileno = len(files) #because files are consecutively named, the number of files should equal the maximum index
    for part in range(fileno):
        file_path = input_data_dir / f"output_{part}.json"
        with open(file=file_path, mode="r") as json_file:
            hadamard_matrices_in_file = json.load(json_file)
        for hadamard_doc in hadamard_matrices_in_file:
            k = hadamard_doc["k"]
            hadamard_matrices.append(hadamard_doc["hadamard_product"])
            sequences.extend([hadamard_doc["seq_id1"], hadamard_doc["seq_id2"]])

    sequences = list(set(sequences))
    print(
        f"Gathered hadamard matrices for {len(hadamard_matrices)} pairs across {len(sequences)} sequences"
    )
    sorted_kmer_score_map = get_all_kmers(
        hadamard_matrices=hadamard_matrices, is_score_weighted=True
    )

    output = {
        "k": k,
        "all_kmers_score_map": sorted_kmer_score_map,
    }
    out_file_path = f"{out_file_dir}/k_{k}.json"
    with open(file=out_file_path, mode="w") as json_file:
        json.dump(output, json_file)
    print(f"Output stored at {out_file_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Read hadamard matrices (reciprocals) for a set of sequences for "
        "a given value of K, and find the best conserved k-mers"
    )
    parser.add_argument(
        "input_data_dir",
        help="Absolute path to directory of hadamard matrices",
        type=str,
    )
    parser.add_argument(
        "out_file_dir",
        type=str,
        help="Absolute path to folder where the conserved k-mers list file (output) is to be stored",
    )
    args = parser.parse_args()

    grantham_subs_matrix_obj = utils.get_grantham_subs_matrix()
    gather_output(
        input_data_dir=args.input_data_dir,
        out_file_dir=args.out_file_dir,
    )
