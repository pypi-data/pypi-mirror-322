"""Run CAPTURE from start to end by means of multiprocessing library for the parallel part"""
import argparse
import datetime
import json
import multiprocessing
import os
import shutil
from pathlib import Path
from typing import Any, List, Mapping, Tuple
import matplotlib; matplotlib.set_loglevel("critical")

from . import *
from .finalize_sharkcapture import (find_kmer_match,
                                    output_top_kmers,
                                    plot_motif_logo,
                                    sort_consensus_kmers_by_length,
                                    update_sequence_dictionary, concatenate_hadamards,
                                    find_kmer_matches_and_add_results_to_output)
from .plotting_functions import *
from .sharkcapture_extended import *
from .logic import get_all_kmers, get_hadamard_matrix
from ..core.utils import (form_sequence_pairs,
                          get_grantham_subs_matrix,
                          read_fasta_file)

TYPE_SCORE_MATRIX = Mapping[str, Mapping[str, float]]
TYPE_SUBS_MATRIX = Tuple[TYPE_SCORE_MATRIX, float, float]


def _parallel_unit(process_arg: List[List[Any]]) -> TYPE_SCORE_MATRIX:
    """Perform hadamard computation for one sequence pair"""
    sequence1: str = process_arg[0]
    sequence2: str = process_arg[1]
    k: int = process_arg[2]
    substitution_matrix_obj: TYPE_SUBS_MATRIX = process_arg[3]
    seq_id1: str = process_arg[4]
    seq_id2: str = process_arg[5]
    hadamard_product = get_hadamard_matrix(
        sequence1=sequence1,
        sequence2=sequence2,
        k=k,
        substitution_matrix=substitution_matrix_obj,
    )

    data_to_save = {
        "seq_id1": seq_id1,
        "seq_id2": seq_id2,
        "sequence1": sequence1,
        "sequence2": sequence2,
        "k": k,
        "substitution_matrix": "grantham",
        "hadamard_product": hadamard_product,
        "created_at": str(datetime.datetime.now()),
    }

    return data_to_save


def prepare_inputs(
    fasta_id_sequence_map: Mapping[str, str],
    substitution_matrix_obj: TYPE_SUBS_MATRIX,
    k: int,
) -> List[List[Any]]:
    """
    Prepare inputs for multiprocessing

    :param(dict) fasta_id_sequence_map: Input set of sequences; Key: Fasta Seq ID; Value: Sequence
    :param(dict of dict, float, float) substitution_matrix_obj: Subs matrix table, Max score, Min score
    :param(int) k: K-Mer length
    :return(list of list): Input params for parallel processes
        0: First sequence
        1: Second sequence
        2: K
        3: Substitution Matrix Object
        4: Sequence ID of First Sequence
        5: Sequence ID of Second Sequence
    """
    seq_pairs_map = form_sequence_pairs(fasta_id_sequence_map)
    process_args = [
        [
            seq_pair_doc["sequence1"],
            seq_pair_doc["sequence2"],
            k,
            substitution_matrix_obj,
            seq_pair_doc["seq_id1"],
            seq_pair_doc["seq_id2"],
        ]
        for seq_pair_doc in seq_pairs_map.values()
    ]

    print(f"Collected args (sequence pairs): {len(process_args)}")
    return process_args


def run_capture_multiprocessing(
    sequence_fasta_file_path: str,
    k_min: int,
    k_max: int,
    output_dir: Path,
    n_output: int,
    outfile: str,
    n_processes: int,
    sequence_subset: list,
    log: bool,
    extend: bool,
    cutoff: float
):
    """
    Core function to run through entire shark-capture pipeline.
    Run reciprocal computation for each sequence pair on a multiprocessing task.
    Gather all reciprocals (hadamard product), and compile into the super dict.
    Output all intermediate matrices and output as json files.

    :param(str) sequence_fasta_file_path: Input set of sequences as FASTA file
    :param(int) k_min: minimum k-mer length
    :param(int) k_max: maximum k-mer length
    :param(Path) output_dir: (root) directory to output all results and intermediate matrices/outputs. Subsequent
    directories will be built within this directory
    :param(int) n_output: number of top consensus k-mers to report
    :param(Path) outfile: filename of output file of top consensus k-mers and their shark-capture score, if provided.
    :param(int) n_processes: number of parallel processes for multi-core processing
    """

    print("Beginning SHARK-CAPTURE")
    id_seq_map = read_fasta_file(file_path=sequence_fasta_file_path)
    grantham_subs_matrix_obj = get_grantham_subs_matrix()

    if os.path.exists(output_dir):
        print("Purging existing {}".format(output_dir))
        shutil.rmtree(output_dir, ignore_errors=True)

    # DEFINE FOLDER STRUCTURES AND CREATE FOLDERS
    input_params_path: Path = output_dir / SUBDIR_INPUT
    conserved_kmers_path: Path = output_dir / SUBDIR_CONSERVED_KMERS
    output_path: Path = output_dir / SUBDIR_OUTPUT
    logos_path: Path = output_dir / SUBDIR_LOGOS
    occurrences_path: Path = output_dir / SUBDIR_OCCURRENCES
    per_sequence_matches_path: Path = output_dir / SUBDIR_PER_SEQUENCE_MATCHES
    hadamards_path: Path = output_dir / SUBDIR_HADAMARDS
    input_params_path.mkdir(parents=True, exist_ok=True)
    conserved_kmers_path.mkdir(parents=True, exist_ok=True)
    logos_path.mkdir(parents=True, exist_ok=True)
    output_path.mkdir(parents=True, exist_ok=True)
    occurrences_path.mkdir(parents=True, exist_ok=True)
    per_sequence_matches_path.mkdir(parents=True, exist_ok=True)
    hadamards_path.mkdir(parents=True, exist_ok=True)

    # DEFINE Score and Occurrence files
    score_file= output_path / outfile
    occurrences_file = occurrences_path / FileNames.ALL_OCCURRENCES_TSV_FILE.value

    """
    RUN SHARK-CAPTURE
    """
    for k in range(k_min, k_max + 1):
        print("\nProcessing {}-mers".format(k))
        hadamard_out_path: Path = hadamards_path /f"hadamard_{k}"
        hadamard_out_path.mkdir(exist_ok=True)
        process_args = prepare_inputs(id_seq_map, grantham_subs_matrix_obj, k=k)
        file_path = input_params_path / f"k_{k}.json"
        input_params = [
            {
                "seq_id1": seq_id1,
                "seq_id2": seq_id2,
                "sequence1": sequence1,
                "sequence2": sequence2,
            }
            for sequence1, sequence2, length, subs_matrix, seq_id1, seq_id2 in process_args
        ]
        param_output = {"k": k, "input_params": input_params}
        with open(file=file_path, mode="w") as json_file:
            json.dump(param_output, json_file)
        print("k={} - Created master input data file at {}".format(k, file_path))
        if not process_args:
            raise Exception("No available sequences for shark-capture runs")
        pool = multiprocessing.Pool(processes=n_processes)
        results = pool.map(_parallel_unit, process_args)
        pool.close()
        print(
            "Completed processing. Gathered hadamard reciprocals for: {}".format(
                len(results)
            )
        )
        hadamard_matrices = [pair["hadamard_product"] for pair in results]
        hadamard_out_file_path = hadamard_out_path / FileNames.ALL_HADAMARDS_JSON_FILE.value
        with open(file=hadamard_out_file_path, mode="w") as json_file:
            json.dump(results, json_file)
        print(
            "Hadamard sorted k-mer score mapping stored at {}".format(hadamard_out_path)
        )

        sorted_kmer_score_map = get_all_kmers(
            hadamard_matrices=hadamard_matrices, is_score_weighted=True
        )
        sorted_kmer_score_map_out_path = conserved_kmers_path / f"k_{k}.json"
        output = {
            "k": k,
            "all_kmers_score_map": sorted_kmer_score_map,
        }
        with open(file=sorted_kmer_score_map_out_path, mode="w") as json_file:
            json.dump(output, json_file)
        print(
            f"Hadamard sorted k-mer score mapping stored at {sorted_kmer_score_map_out_path}"
        )

    # FIND TOP CONSENSUS K-MERS
    consensus_kmers_list = output_top_kmers(
        conserved_kmers_path, k_min, k_max, n_output, score_file
    )
    print(f"Reporting top {n_output} K-Mers, stored in {score_file}")

    # MAP CONSENSUS K-MERS TO SEQUENCES AND PLOT MOTIF LOGOS
    output_data = ["sequenceID\treference_kmer\tmatch\tstart\tend\n"]

    length_tracker = 0
    hadamards_data = []
    seq_dict = {}
    consensus_kmer_length_group = []
    all_hadamards_data: dict = concatenate_hadamards(hadamards_path, k_min, k_max)
    for consensus_kmer, sharkcapture_score in sort_consensus_kmers_by_length(consensus_kmers_list):
        consensus_kmer_length = len(consensus_kmer)
        if length_tracker < consensus_kmer_length:
            find_kmer_matches_and_add_results_to_output(
                output_data,
                occurrences_path,
                consensus_kmer_length_group,
                hadamards_data,
                seq_dict,
            )
            length_tracker = consensus_kmer_length
            hadamards_data = all_hadamards_data.get(consensus_kmer_length)
            seq_dict = update_sequence_dictionary(hadamards_data)
            consensus_kmer_length_group = [consensus_kmer]
        else:
            consensus_kmer_length_group.append(consensus_kmer)
    find_kmer_matches_and_add_results_to_output(
        output_data,
        occurrences_path,
        consensus_kmer_length_group,
        hadamards_data,
        seq_dict,
    )
    with open(occurrences_file, "w+") as f:
        f.writelines(output_data)
    for consensus_kmer, sharkcapture_score in consensus_kmers_list:
        (
            frequency_df,
            probability_df,
            information_content_df,
            conservation_info,
        ) = plot_motif_logo(
            occurrences_path / f"sharkcapture_{consensus_kmer}_occurrences.tsv", logos_path
        )

    #PERFORM EXTENSION PROCEDURE IF DESIRED
    if extend:
        print('Performing SHARK-capture Extension Procedure...')
        merged_df = merge_match_and_score_files(
            sharkcapture_score_filepath = score_file,
            kmer_occurrence_filepath = occurrences_file,
            save=True
        )
        extended_df = collapse_to_core_kmers(
            full_df=merged_df,
            score_cutoff_prop= cutoff,
            save=True,
            simplified=True,
            outfile_path= occurrences_path / FileNames.ALL_OCCURRENCES_EXTENDED_TSV_FILE.value
        )
        print('SHARK-capture Extension Procedure Complete')

    #FOR EACH SEQUENCE IN SEQUENCE-SUBSET, PLOT PER-SEQUENCE K-MER MATCHES
    for sequence_id in sequence_subset:
        per_sequence_plot=plot_residue_scores(
            fasta_filepath=sequence_fasta_file_path,
            sequence_ID= sequence_id,
            sharkcapture_score_filepath= score_file,
            kmer_occurrence_filepath= occurrences_file,
            outpath=per_sequence_matches_path / sequence_id.replace('|','_').replace('/','_').replace('.','_'),
            n_kmers_to_plot= n_output,
            save_data=True,
            show=False,
            log= log
        )
        print(f'top {n_output} K-mer matches in {sequence_id} saved to {per_sequence_matches_path}')

    #COMPLETION
    print(
        "\nAll outputs stored in {}.\n\nSHARK-capture completed successfully!".format(
            output_dir
        )
    )


def main():
    parser = argparse.ArgumentParser(
        description="SHARK-capture: "
                    "An alignment-free, k-mer physicochemical similarity-based motif detection tool"
    )
    parser.add_argument(
        "sequence_fasta_file_path",
        help="Absolute path to fasta file of input sequences",
        type=str,
    )
    parser.add_argument("output_dir", help="Output folder path", type=str)
    parser.add_argument(
        "--outfile",
        help="name of consensus k-mers output file",
        type=str,
        default="sharkcapture_consensus_kmers.txt",
    )
    parser.add_argument(
        "--k_min", help="Min k-mer length of captured motifs", type=int, default=3
    )
    parser.add_argument(
        "--k_max", help="Max k-mer length of captured motifs", type=int, default=10
    )
    parser.add_argument(
        "--n_output",
        help="number of top consensus k-mers to output and process for subsequent steps",
        type=int,
        default=10,
    )
    parser.add_argument(
        "--n_processes",
        help="No. of processes (python multiprocessing",
        type=int,
        default=8,
    )
    parser.add_argument(
        "--log", help="flag to show scores in log scale (base 10) for per-sequence k-mer matches plot",
        action='store_true'
    )
    parser.add_argument(
        "--extend", help="enable SHARK-capture Extension Protocol",
        action='store_true'
    )
    parser.add_argument(
        "--cutoff",
        help="Percentage cutoff for SHARK-capture Extension Protocol, default 0.9",
        type=float,
        default=0.9,
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--no_per_sequence_kmer_plots", help="flag to suppress plotting of per-sequence k-mer matches."
        "Mutually exclusive with --sequence_subset",
        action='store_true'
    )
    group.add_argument(
        "--sequence_subset", help="comma separated sequence identifiers or substrings to generate output"
                                  ' for per-sequence k-mer matches plot, e.g. "sequence_id_1,sequence_id_2". '
                                    "By default, plots for all sequences. "
                                    "Mutually exclusive with --no_per_sequence_kmer_plots.",
        type=str,
        default='all'
    )

    args = parser.parse_args()

    sequence_subset_ls = []
    if not args.no_per_sequence_kmer_plots:
        if args.sequence_subset=='all':
            sequence_subset_ls.extend(list(read_fasta_file(file_path=args.sequence_fasta_file_path).keys()))
        elif args.sequence_subset:
            sequence_subset_ls.extend(args.sequence_subset.split(","))

    run_capture_multiprocessing(
        sequence_fasta_file_path=args.sequence_fasta_file_path,
        k_min=args.k_min,
        k_max=args.k_max,
        output_dir=Path(args.output_dir),
        n_output=args.n_output,
        outfile=args.outfile,
        n_processes=args.n_processes,
        sequence_subset=sequence_subset_ls,
        log=args.log,
        extend=args.extend,
        cutoff=args.cutoff,
    )


if __name__ == "__main__":
    main()
