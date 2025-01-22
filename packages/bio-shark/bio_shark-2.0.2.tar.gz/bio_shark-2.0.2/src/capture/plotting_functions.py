"""
Example usage when imported:

    consensus_kmer_matches_folder=Path('path/to/consensus/kmer/matches/')
    concatenated_kmer_occurence_filepath=Path('path/to/aggregated/kmer/occurence/file')

    concatenate_kmer_matches_files(consensus_kmer_matches_folder, concatenated_kmer_occurence_filepath)

    fasta_filepath=Path('path/to/fasta/file.fasta')
    sequence_ID='sequence_ID'
    sharkcapture_score_filepath=Path('path/to/sharkcapture/score/file')
    output_file=Path('path/to/save/visualisation/file')
    n_kmers_to_plot= 100
    save_data= True
    show= False
    log= False

    max_sharkcapture_score_per_residue=plot_residue_scores(
    fasta_filepath=fasta_filepath,
    sequence_ID=sequence_ID,
    sharkcapture_score_filepath=sharkcapture_score_filepath,
    kmer_occurrence_filepath=concatenated_kmer_occurence_filepath,
    outpath=output_file,
    n_kmers_to_plot=n_kmers_to_plot,
    save_data=save_data,
    show=show,
    log=log
    )
"""


import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from pathlib import Path
import argparse

from ..core.utils import read_fasta_file
from .capture_utils import concatenate_kmer_matches_files, merge_match_and_score_files


def plot_residue_scores(fasta_filepath: Path, sequence_ID: str, sharkcapture_score_filepath: Path,
                        kmer_occurrence_filepath: Path, outpath: Path, n_kmers_to_plot: int, save_data: bool = False,
                        show: bool = False, log: bool = False):
    """
    Visualize detected, conserved k-mers in a sequence, color-coded by its shark-capture score

    :param(Path) fasta_filepath: Path to input sequence file for the shark-capture run
    :param(str) sequence_ID: identifier of the sequence to map k-mers on. Should be identical to a sequence ID
    in the input sequence file
    :param(Path) sharkcapture_score_filepath: Path to (tab-separated) file of (ranked) consensus k-mers and their
    shark-capture score
    :param(Path) kmer_occurrence_filepath: Path to concatenated (tab-separated) file of mapped motif occurrences
    across all consensus k-mers to be mapped to the sequence
    :param(Path) outpath: Path to save visualization plot
    :param(int) n_kmers_to_plot: number of detected k-mers to map
    :param(bool) save_data: if True, save data as {outpath}.csv
    :param(bool) show: if True, show plot on screen

    :return(pd.DataFrame): pd.DataFrame object of the maximum shark-capture score of each residue in the sequence.
    Note that per our convention, masked residues have a shark-capture score of -1 and
    undetected residues have a score of 0
    """

    # READ IN FILES
    seqs = read_fasta_file(file_path=fasta_filepath)

    # MERGE SCORE AND OCCURRENCE FILES
    kmer_df = merge_match_and_score_files(sharkcapture_score_filepath, kmer_occurrence_filepath, n_kmers_to_plot)
    kmer_df.sort_values('sharkcapture_score', ascending=False, inplace=True)

    # SELECT SEQUENCE AND FILTER DATAFRAME FOR SEQUENCE
    sequence = seqs[sequence_ID]
    kmer_df = kmer_df[kmer_df['sequenceID'] == sequence_ID]

    # GET MAX SHARK-CAPTURE SCORE PER RESIDUE
    per_residue_max_score = dict()
    for i in range(1, len(sequence) + 1):
        if sequence[i - 1] == '*':
            per_residue_max_score[i] = -1
        else:
            if list(kmer_df[(kmer_df['start'] <= i) & (kmer_df['end'] >= i)]['sharkcapture_score']):  # can only
                max_val = max(list(kmer_df[(kmer_df['start'] <= i) & (kmer_df['end'] >= i)]['sharkcapture_score']))
                per_residue_max_score[i] = max_val
            else:
                per_residue_max_score[i] = 0

    # CONVERT PER_RESIDUE_MAX_SCORE INTO A DATAFRAME
    per_residue_max_score_list = [{'Position': k, 'Residue': sequence[k - 1], 'maximum_sharkcapture_score': v} for k, v
                                  in per_residue_max_score.items()]
    per_residue_max_score_df = pd.DataFrame(per_residue_max_score_list)

    # SAVE DATAFRAME IF NECESSARY
    if save_data:
        print(f'Saving data to {outpath}.csv')
        per_residue_max_score_df.to_csv(str(outpath) + '.csv', index=False)

    # CONVERT SCORES TO LOG IF NECESSARY
    if log:
        # MASKING RESIDUES AND UNDETECTED RESIDUES NOW GET A SCORE OF 1 SINCE LOG(1)=0.
        per_residue_max_score_log = dict()
        for k,v in per_residue_max_score.items():
            if v>0:
                per_residue_max_score_log[k] = v
            else:
                per_residue_max_score_log[k] = 1
        per_residue_max_score_list = [{'Position': k, 'Residue': sequence[k - 1], 'maximum_sharkcapture_score': v} for
                                      k, v
                                      in per_residue_max_score_log.items()]
        per_residue_max_score_df = pd.DataFrame(per_residue_max_score_list)
        per_residue_max_score_df['maximum_sharkcapture_score'] = np.log10(per_residue_max_score_df['maximum_sharkcapture_score'])

    # SET UP COLORBAR
    cmap = sns.color_palette("blend:#FFF,#4EB2C8,#955574", as_cmap=True)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0, vmax=per_residue_max_score_df[
        ['maximum_sharkcapture_score']].max()))

    # PLOTTING TIME! PLOT MAX SHARK-CAPTURE SCORE PER RESIDUE
    protein_seq = list(sequence)
    n_plots = max([(len(protein_seq) // 100), 3]) # minimum no. plots = 3 or else I get a matplotlib aspect error
    padding = int(n_plots // 3)  # just to make the color bar not overlap with the plot
    vert_size= int(0.7*n_plots) # just a scaling factor to make the plot look a bit nicer

    figure, axes = plt.subplots(figsize=(15, vert_size))

    axes.set_visible(False)
    figure.suptitle('SHARK-capture detected regions in %s' % (sequence_ID))
    axes.patch.set_visible(False)

    prev_start = 0
    counter = 1

    if len(protein_seq) % 100 != 0:
        n_plots += 1
    for i in range(100, len(protein_seq) + 100, 100):
        ax = figure.add_subplot(n_plots + padding, 1, counter)
        heatmap = sns.heatmap(data=per_residue_max_score_df[['maximum_sharkcapture_score']][prev_start:i].transpose(),
                              xticklabels=[], ax=ax, cbar=False, square=False,
                              annot=np.array([*protein_seq[prev_start:i]]).reshape(1, -1), fmt='',
                              cmap=sns.color_palette("blend:#FFF,#4EB2C8,#955574", as_cmap=True),
                              vmin=0,
                              vmax=per_residue_max_score_df[['maximum_sharkcapture_score']].max()
                              )
        ax.set_yticks([0.5], labels=[prev_start + 1], rotation=0)
        ax.set_xticks([0, 100], labels=['', ''])
        ax.tick_params(axis='both', which='both', length=0)
        counter += 1
        prev_start = i

    # APPEND COLORBAR
    label= 'log(maximum shark-capture score)' if log else 'maximum shark-capture score'
    plt.colorbar(sm, ax=axes, location="bottom", shrink=0.5, label=label)

    # SAVE FIGURES
    print(f'saving figure as {outpath}')
    plt.savefig(outpath, dpi=600)
    plt.savefig(str(outpath) + '.svg', format='svg')

    # SHOW PLOT IF NECESSARY
    if show:
        plt.show()

    plt.close()

    return per_residue_max_score_df




if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="SHARK-capture Visualization Toolkit: "
        "Plotting functions to visualize SHARK-capture matches in a sequence, "
        "color-coded by maximum SHARK-capture score per residue. "
        "First aggregates all k-mer occurrences into one large file (can be disabled)."
    )
    parser.add_argument(
        "concat",
        help="Absolute path to file for saving aggregated shark-capture matches. "
        "If the aggregated file is not present, pass the --folder to aggregate individual occurrence files {sharkcapture_motif_occurrences.tsv}"
        "Otherwise (if the aggregated file is already present), pass that file and use the --no_agg flag to disable aggregation step."
        ,
        type=str,
    )
    parser.add_argument(
        "fasta",
        help="Absolute path to input fasta file containing the sequence",
        type=str,
    )
    parser.add_argument(
        "seqid",
        help="Sequence ID, must match that in input fasta file",
        type=str,
    )
    parser.add_argument(
        "scores",
        help="Absolute path to file containing top consensus k-mers and their shark-capture scores",
        type=str,
    )
    parser.add_argument("n", help="number of k-mers to plot."
    "Should be less than or equal to the number of consensus k-mers in the score file."
    "Otherwise, all consensus k-mer matches will be plotted", type=int)
    parser.add_argument(
        "outfile", help="name of visualization plot file."
        "The plot will be saved in the folder containing the aggregated shark-capture matches.",
        type=str
    )
    parser.add_argument(
        "--save", help="flag to enable saving of per-residue maximum shark-capture store data"
        "as a table",
        action='store_true'
    )
    parser.add_argument(
        "--show", help="flag to show plot on screen",
        action='store_true'
    )
    parser.add_argument(
        "--log", help="flag to show scores in log scale (base 10)",
        action='store_true'
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--folder",
        help="Absolute path to folder containing mapped shark-capture matches if aggregation is necessary",
        type=str
    )
    group.add_argument(
        "--noagg", help="flag to disable the aggregation of k-mer occurrence files, "
        "for example if the file has already been aggregated. "
        "In this case, the <concat> file is used directly",
        action='store_true'
    )
    args = parser.parse_args()

    aggregate_p: Path = Path(args.concat)
    fasta_p: Path = Path(args.fasta)
    outfile_p: Path = args.outfile
    scores_p: Path = Path(args.scores)

    # run functions
    if not args.noagg:
        aggregate_p.parents[0].mkdir(parents=True, exist_ok=True)
        concatenate_kmer_matches_files(Path(args.folder), aggregate_p)
    max_sharkcapture_score_per_residue=plot_residue_scores(
    fasta_filepath=fasta_p,
    sequence_ID=args.seqid,
    sharkcapture_score_filepath=scores_p,
    kmer_occurrence_filepath=aggregate_p,
    outpath= aggregate_p.parents[0]/ outfile_p,
    n_kmers_to_plot=args.n,
    save_data= args.save,
    show= args.show,
    log= args.log
    )
