"""
Example usage when imported:

    folder_path=Path('path_to_folder_containing_hadamard_matrices_and_conserved_kmers')
    output_file=Path('consensus_kmers_file')
    kmin=3
    kmax=10
    n=10
    concatenate_hadamards(folder_path,kmin,kmax)
    top1list=output_top_kmers(folder_path / 'conserved_kmers',kmin,kmax,n,folder_path / output_file)
    top1=top1list[0][0]
    print(folder_path,top1list)
    res=find_kmer_match(folder_path,top1)
    frequency_df,probability_df,information_content_df,conservation_info=plot_motif_logo(folder_path / 'sharkcapture_'+top1+'_occurrences.tsv',folder_path)

"""
import argparse
import collections as clt
import glob
import json
import math
from pathlib import Path
import matplotlib; matplotlib.set_loglevel("critical")
import warnings

import matplotlib.pyplot as plt
import pandas as pd

import logomaker

from . import *


def find_kmer_match(folder_path: Path, motifs: list, hadamards_data: dict, seq_dict: dict, output=True,
                    seqid_subset=None):
    """
    Map consensus k-mers back onto sequences if reciprocal match exists. If multiple reciprocal matches (k-mers) exist,
    choose k-mer based on highest number of reciprocal matches, then find all instances of that k-mer in the sequence

    :param(Path) folder_path: Path to result output folder.
    :param(str) motif: consensus k-mer with which to map back to sequence
    :param(bool) output: whether to output the results of the consensus k-mer sequence mapping to a tab-separated table
    with name sharkcapture_{consensus k-mer}_occurrences.tsv, default True
    :return(dict[str, dict[str, set(tuple([str, int, int]]]): (Outer) Key -> consensus k-mer, Value -> dictionary where:
    (Inner) Key -> Sequence ID; Value -> A set of amino acid coordindates,
    in the format of(matched k-mer, start, end). Note that amino acid coordinates are 1-indexed.
    """
    if not motifs:
        return {}
    sequence_match_infos = clt.defaultdict(
        dict, set()
    )  # keys: sequence id, values: best match kmer and coordinates as tuple (kmer, start, end)

    lencheck = set()
    for seqid, sequence in seq_dict.items():
        if seqid_subset is not None and not any([x for x in seqid_subset if x in seqid]):
            continue
        match_counts = clt.defaultdict(dict)
        # keys: k-mers in sequence, values: number of times the k-mer matches the reference k-mer reciprocally
        hadamard_subset = [
            pair
            for pair in hadamards_data
            if pair["seq_id1"] == seqid or pair["seq_id2"] == seqid
        ]
        lencheck.add(len(hadamard_subset))

        for pair_subset in hadamard_subset:
            for motif in motifs:
                if (
                        pair_subset["seq_id1"] == seqid
                ):  # self k-mers are in the outer-dict, k-mers in other sequence are in inner dict
                    for kmer_self, kmer_dict_other in pair_subset[
                        "hadamard_product"
                    ].items():
                        for kmer_other, similarity_value in kmer_dict_other.items():
                            if kmer_other == motif:
                                try:
                                    match_counts[motif][kmer_self] += 1
                                except KeyError:
                                    match_counts[motif][kmer_self] = 1
                elif (
                        pair_subset["seq_id2"] == seqid
                ):  # k-mers in other sequence are in the outer dict, self k-mers are in inner dict
                    for kmer_other, kmer_dict_self in pair_subset[
                        "hadamard_product"
                    ].items():
                        if kmer_other == motif:
                            for kmer_self, similarity_value in kmer_dict_self.items():
                                try:
                                    match_counts[motif][kmer_self] += 1
                                except KeyError:
                                    match_counts[motif][kmer_self] = 1
                else:
                    print(  # noqa: T201
                        seqid + "not in hadamard_subset, something is terribly wrong"
                    )

        for motif in match_counts:
            match_count = match_counts[motif]

            if match_count:  # only run if match_count is not an empty dict
                max_count = max(match_count.values())
                max_count_matches = [
                    kmer for kmer, count in match_count.items() if count == max_count
                ]  # only get k-mers in the sequence that have max reciprocal matches to the reference k-mer

                best_match = max_count_matches[0]
                for i in range(
                        len(sequence) - len(motif) + 1
                ):  # it would be impossible for len(best_match)!=len(motif)
                    if sequence[i: i + len(motif)] == best_match:
                        try:
                            sequence_match_infos[motif][seqid].add(
                                tuple([best_match, i + 1, i + len(motif)])
                            )  # positions are 1-indexed
                        except KeyError:
                            sequence_match_infos[motif][seqid] = set()
                            sequence_match_infos[motif][seqid].add(
                                tuple([best_match, i + 1, i + len(motif)])
                            )  # positions are 1-indexed
            else:
                continue

    if len(lencheck) != 1:
        print("not all pairs considered")  # noqa: T201

    if output:
        for motif in sequence_match_infos:
            print(f"Writing SHARK-capture occurrences for {motif} into {folder_path} ...")
            with open(folder_path / f"sharkcapture_{motif}_occurrences.tsv", "w+") as f:
                f.write("sequenceID\treference_kmer\tmatch\tstart\tend\n")
                sequence_matches = sequence_match_infos[motif]
                for seqid, occurrences in sequence_matches.items():
                    for match, start, end in occurrences:
                        f.write(
                            seqid
                            + "\t"
                            + motif
                            + "\t"
                            + match
                            + "\t"
                            + str(start)
                            + "\t"
                            + str(end)
                            + "\n"
                        )
    return sequence_match_infos


def output_top_kmers(
        folder_with_sorted_kmer_map: Path,
        kmin: int,
        kmax: int,
        n,
        outfile: Path = None,
):
    """
    Report most conserved consensus k-mers across range of k's by scaling the raw score from the summed hadamard matrix
    with the search space factor, which is dependent on the number of unique k-mers in the set for a given value of k.

    :param(Path) folder_with_sorted_kmer_map: Path to result output folder where the summed matrices are scored.
    For now it is hard-coded that the summed matrices are named k_{k}.json
    :param(int) kmin: minimum k-mer length
    :param(int) kmax: maximum k-mer length
    :param(int) n: number of top consensus k-mers to report
    :param(Path) outfile: filename of output file of top consensus k-mers and their shark-capture score, if provided.
    :return(list of tuples[str, int]): Each tuple gives the consensus k-mer and its corresponding shark-capture score.
    List is sorted in descending order of shark-capture score.
    """
    per_k_scoredict = {}
    for k in range(kmin, kmax + 1, 1):
        with open(
                folder_with_sorted_kmer_map / f"k_{k}.json"
        ) as json_file:  # name of output file hardcoded for now
            data = json.load(json_file)
        per_k_scoredict[k] = data["all_kmers_score_map"]
    for k, scoredict in per_k_scoredict.items():
        sorteddict = sorted(scoredict.items(), reverse=True, key=lambda x: x[1])
        per_k_scoredict[k] = sorteddict

    searchspace = dict()
    for k, scoredict in per_k_scoredict.items():
        searchspace[k] = math.sqrt(len(scoredict))  # implement search space factor

    allscores = [
        (kmer, score * searchspace[len(kmer)])
        for scoredict in per_k_scoredict.values()
        for kmer, score in scoredict
    ]
    allscores = sorted(allscores, reverse=True, key=lambda x: x[1])

    if type(n) is float:
        n = int(round(len(allscores) * n))
    if outfile:
        with open(outfile, "w") as f:
            f.write("consensus,sharkcapture_score\n")
            for consensus_kmer, finalscore in allscores[:n]:
                f.write(consensus_kmer + "," + str(finalscore) + "\n")

    return allscores[:n]


def concatenate_hadamards(folder_path: Path, kmin: int, kmax: int) -> dict:
    """
    For HPC-parallelised runs: to aggregate all partial outputs into one file containing all hadamard matrices.
    Required for subsequent mapping steps (find_kmer_match)

    :param(Path) folder_path: Path to output folder where the hadamard matrices (from pairwise comparisons) are stored.
    For now it is hard-coded that the folder with the hadamard matrices is called hadamard_$length
    :param(int) kmin: minimum k-mer length
    :param(int) kmax: maximum k-mer length
    """
    print("Loading hadamards...")
    all_hadamards_data = {}
    for i in range(kmin, kmax + 1, 1):
        final = []
        hadamards_file: Path = folder_path / f"hadamard_{i}" / FileNames.ALL_HADAMARDS_JSON_FILE.value
        if hadamards_file.exists():
            print(f"Found file {FileNames.ALL_HADAMARDS_JSON_FILE.value} for k={i}")  # noqa: T201
            with hadamards_file.open() as f:
                data = json.load(f)
                final.extend(data)
        else:
            print(f"Could not find file {FileNames.ALL_HADAMARDS_JSON_FILE.value} for k={i}")  # noqa: T201
            search_path = folder_path / f"hadamard_{i}/output_*.json"
            li = [elem for elem in glob.glob(f"{search_path}")]
            print(f"There are {len(li)} output files at k={i}")  # noqa: T201
            for part in range(len(li)):
                file = folder_path / f"hadamard_{i}/output_{part}.json"
                with open(
                        file
                ) as json_file:  # for now it is hard-coded that the folder with the hadamard matrix is called hadamard_$length
                    data = json.load(json_file)
                final.extend(data)
            with open(hadamards_file, "w") as f:
                json.dump(final, f)

        all_hadamards_data[i] = final
    return all_hadamards_data


def plot_motif_logo(df: Path, outfolder: Path, suppress_warnings: bool = True):
    """
    For a given consensus k-mer and its mapped occurrences in the set of sequences, construct a 'motif logo' as a visual
    representation of the consensus k-mer. The motif logo is generated from the full set of occurrences as a probability
    matrix, including pseudocounts, using the logomaker package.

    :param(Path) df: path to file containing occurrences of consensus k-mer.
    By default it is called sharkcapture_{consensus k-mer}_occurrences.tsv as per output of find_kmer_match.
    :param(Path) outfolder: path to folder to output probability matrix and logo files, if provided.
    :return(tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]): frequency matrix, probability matrix,
    information content matrix, summed information content matrix by position
    (i.e. degree of conservation of the position)
    """
    df = pd.read_csv(df, sep="\t")

    filter_list = list("ACDEFGHILKMNPQRSTVWY")
    motifs = df["reference_kmer"].unique()

    if suppress_warnings:
        warnings.filterwarnings('ignore', module='logomaker')

    if len(motifs) < 1:
        print("no motifs")  # noqa: T201
    elif len(motifs) > 1:
        print("multiple motifs")  # noqa: T201

    for motif in motifs:
        dictlist = [dict.fromkeys(filter_list, 0) for i in range(len(motif))]
        for i in range(len(motif)):
            for kmer_match in df["match"]:
                aa = kmer_match[i]
                dictlist[i][aa] += 1

        freq_df = pd.DataFrame(dictlist)
        ic_df = logomaker.transform_matrix(
            freq_df, from_type="counts", to_type="information"
        )
        prob_df = logomaker.transform_matrix(
            freq_df, from_type="counts", to_type="probability"
        )

        if outfolder:
            fig = logomaker.Logo(ic_df)
            plt.title(motif, fontsize=12)
            plt.ylabel("Information Content", fontsize=11)
            plt.savefig(outfolder / f"{motif}_logo", dpi=300)
            plt.close()
            prob_df.to_csv(outfolder / f"{motif}_probabilitymatrix.csv")

        return freq_df, prob_df, ic_df, ic_df.sum(axis=1)


def sort_consensus_kmers_by_length(consensus_kmers_list: list) -> list:
    """Sorts list of consensus kmers by length and returns a new sorted list."""
    return sorted(consensus_kmers_list, reverse=False, key=lambda x: len(x[0]))


# @timeit
def update_sequence_dictionary(data):
    """Transform data format from JSON to dictionary and extract sequence pairs."""
    print("Updating sequence dictionary...")
    seq_dict = {}
    for pair in data:
        seq_dict[pair["seq_id1"]] = pair["sequence1"]
        seq_dict[pair["seq_id2"]] = pair["sequence2"]
    return seq_dict


# @profile(stdout=False, filename='finalize_sharkcapture.prof')
def find_kmer_matches_and_add_results_to_output(
        output_data,
        folder_path: Path,
        motifs: list,
        hadamards_data: dict,
        seq_dict: dict,
        seqid_subset: list = None,
        output: bool = True,
):
    sequence_matches_dict: dict = find_kmer_match(
        folder_path,
        motifs,
        hadamards_data,
        seq_dict,
        seqid_subset=seqid_subset,
        output=output
    )
    for motif in sequence_matches_dict:
        sequence_matches = sequence_matches_dict[motif]
        for seqid, occurrences in sequence_matches.items():
            for match, start, end in occurrences:
                output_data.append(f"{seqid}\t{motif}\t{match}\t{start}\t{end}\n")


def main(args):
    folder_p: Path = Path(args.folder)
    hadamards_p: Path = folder_p / "intermediates" / "hadamards"
    if args.hadamards:
        hadamards_p: Path = Path(args.hadamards)
    conserved_kmers_p: Path = folder_p / "intermediates" / "conserved_kmers"
    if args.conserved:
        conserved_kmers_p: Path = Path(args.conserved)
    outfile_p: Path = folder_p / "outputs"
    if args.outfolder:
        outfile_p: Path = Path(args.outfolder)
    occurrences_p: Path = outfile_p / "occurrences"
    logos_p: Path = outfile_p / "logos"

    for folder in [outfile_p, occurrences_p]:
        folder.mkdir(parents=True, exist_ok=True)
    if not args.no_logos:
        logos_p.mkdir(parents=True, exist_ok=True)

    all_hadamards_data: dict = concatenate_hadamards(hadamards_p, args.kmin, args.kmax)

    # TODO I wanted to have a relative cutoff too but I don't know if this is the best implementation
    try:
        n_output = int(args.n_output)
    except ValueError:
        n_output = float(args.n_output)

    consensus_kmers_list = output_top_kmers(
        conserved_kmers_p,
        args.kmin,
        args.kmax,
        n_output,
        outfile_p / args.outfile,
    )
    if args.sequence_subset is not None:
        sequence_subset_ls = args.sequence_subset.split(",")
    else:
        sequence_subset_ls = None

    output_data = ["sequenceID\treference_kmer\tmatch\tstart\tend\n"]

    length_tracker = 0
    data = []
    seq_dict = {}
    consensus_kmer_length_group = []
    for consensus_kmer, sharkcapture_score in sort_consensus_kmers_by_length(consensus_kmers_list):
        consensus_kmer_length = len(consensus_kmer)
        if length_tracker < consensus_kmer_length:
            find_kmer_matches_and_add_results_to_output(
                output_data=output_data,
                folder_path=occurrences_p,
                motifs=consensus_kmer_length_group,
                hadamards_data=data,
                seq_dict=seq_dict,
                seqid_subset=sequence_subset_ls,
                output=not args.no_separate
            )
            length_tracker = consensus_kmer_length
            data = all_hadamards_data.get(consensus_kmer_length)
            seq_dict = update_sequence_dictionary(data)
            consensus_kmer_length_group = [consensus_kmer]
        else:
            consensus_kmer_length_group.append(consensus_kmer)

    find_kmer_matches_and_add_results_to_output(
        output_data=output_data,
        folder_path=occurrences_p,
        motifs=consensus_kmer_length_group,
        hadamards_data=data,
        seq_dict=seq_dict,
        seqid_subset=sequence_subset_ls,
        output=not args.no_separate
    )

    with open(occurrences_p / "all_occurrences.tsv", "w+") as f:
        f.writelines(output_data)


    if not args.no_logos:
        for consensus_kmer, sharkcapture_score in consensus_kmers_list:
            (
                frequency_df,
                probability_df,
                information_content_df,
                conservation_info,
            ) = plot_motif_logo(
                occurrences_p / f"sharkcapture_{consensus_kmer}_occurrences.tsv",
                logos_p
            )
    print("Program finished successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="SHARK-capture Final Steps: "
                    "aggregate individual outputs from parallel runs to a final reciprocal matrix file"
                    "From reciprocal matrices, find top consensus k-mers"
                    "Map consensus k-mers back to sequences"
    )
    parser.add_argument(
        "folder",
        help="Path to root folder containing all data and where outputs should be stored."
        "By default, all data used should be in the intermediates folder, with a separate folder for the list of"
        " conserved k-mers, and a separate folder for the reciprocal matches/hadamards."
        "The hadamards folder should contain, for each k-mer length, a separate folder as hadamard_k."
        "If the a different folder structure is used, please specify in the --hadamards and --conserved flags",
        type=str,
    )
    parser.add_argument("kmin", help="minimum k-mer length", type=int)
    parser.add_argument("kmax", help="maximum k-mer length", type=int)
    parser.add_argument(
        "n_output",
        help="number of top consensus k-mers to output and process for subsequent steps. if float use proportion of top k-mers instead."
    )
    parser.add_argument(
        "outfile", help="Path to consensus k-mers output file."
    "By default the file is stored in <folder>/output/, unless the --outfolder argument is also passed.", type=str
    )
    parser.add_argument(
        "--sequence_subset", help="comma separated sequence identifiers or substrings to generate output for", type=str,
        default=None
    )
    parser.add_argument(
        "--no_logos", help="flag to suppress output of motif logos and detailed information", action='store_true'
    )
    parser.add_argument(
        "--no_separate", help="flag to suprress the output each set of consensus k-mer matches as a separate file", action='store_true',
        default=None
    )
    parser.add_argument(
        "--hadamards",
        help="Path to folder containing the hadamard matrices folders in the form <hadamard_k>, default: folder/intermediates/hadamards",
        type=str,
        default=None
    )
    parser.add_argument(
        "--conserved",
        help="Path to folder containing conserved k-mers information as json files, default: folder/intermediates/conserved",
        type=str,
        default=None
    )
    parser.add_argument(
        "--outfolder",
        help="Path to folder to store outputs, default: folder/outputs",
        type=str,
        default=None
    )

    args = parser.parse_args()
    main(args)
