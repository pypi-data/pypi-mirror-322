import glob
import pandas as pd
from pathlib import Path


def concatenate_kmer_matches_files(folder_path, outfile_path):
    """
    Aggregates all k-mer occurrence files (1 per consensus k-mer) within the folder into one large file.
    Purely for convenience/formatting purposes.


    :param(Path) folder_path: Path to folder containing the occurrence files. Here it is assumed that the files are
    named as sharkcapture_{motif}_occurrences.tsv and are tab-separated
    :param(Path) outfile_path: Output file path

    :return(pd.DataFrame): DataFrame containing sequenceID, reference_kmer, sequence match, and start and end
    coordinates of the match

    """
    outfile = pd.DataFrame()
    for elem in glob.glob(str(folder_path) + '/sharkcapture_*_occurrences.tsv'):
        outfile = pd.concat([outfile, pd.read_csv(elem, sep='\t')])
    outfile.to_csv(outfile_path, sep='\t', index=False)

    return outfile

def merge_match_and_score_files(sharkcapture_score_filepath: Path, kmer_occurrence_filepath: Path,
                                top_n: int = -1, save: bool = False, outfile_path: Path = None):
    """
    Merges sharkcapture_score_filepath, kmer_occurrence_filepath, top_n and save

    :param (Path) sharkcapture_score_filepath: file path to sharkcapture score file
    :param (Path) kmer_occurrence_filepath: file path to kmer occurrence file
    :param (int) top_n: number of consensus k-mers to merge between match and score file
    :param (Bool) save: whether or not to save the merged score file (default False)
    :param (Path) outfile_path: path to save the merged score file (default None). If not given and save=True,
    save as occurrence file+.merged.tsv

    :return (DataFrame): kmer_df
    """


    # since consensus and reference k-mers mean the same thing, this just makes the merging a bit cleaner
    sharkcapture_score = pd.read_csv(sharkcapture_score_filepath, skiprows=1, names=['reference_kmer',
                                                                                     'sharkcapture_score'])
    kmer_occurrence = pd.read_csv(kmer_occurrence_filepath, sep='\t')

    # CHECK THAT SCORE FILE IS PROPERLY RANKED, THEN FILTER FOR TOP N K-MERS TO PLOT (OPTIONAL), ELSE MERGE ALL
    if sharkcapture_score['sharkcapture_score'].is_monotonic_decreasing:
        if top_n > -1:
            sharkcapture_score = sharkcapture_score.loc[0:top_n - 1, :]
    else:
        print('score file has been modified')
        sharkcapture_score.sort_values('sharkcapture_score', ascending=False, inplace=True)
        if top_n > -1:
            sharkcapture_score = sharkcapture_score.loc[0:top_n - 1, :]

    # MERGE SCORE AND OCCURRENCE FILES
    kmer_df = kmer_occurrence.merge(sharkcapture_score, on='reference_kmer', how='inner')

    # RETAIN ORDER OF ORIGINAL SCOREFILE (RANKED K-MERS). THIS IS IN MOST CASES UNIMPORTANT,
    # ONLY USEFUL IN RARE CASES WHERE THERE ARE IDENTICAL SCORES
    order_dict=dict(zip(sharkcapture_score.reference_kmer,sharkcapture_score.index))
    kmer_df = kmer_df.sort_values(by=['reference_kmer'], key=lambda x: x.map(order_dict))
    kmer_df.reset_index(inplace=True,drop=True)
    if not kmer_df['sharkcapture_score'].is_monotonic_decreasing:
        print('something is horribly wrong')

    if save:
        if outfile_path:
            kmer_df.to_csv(outfile_path, sep='\t', index=False)
        else:
            kmer_df.to_csv(str(kmer_occurrence_filepath)+'.merged.tsv', sep='\t', index=False)

    return kmer_df


def output_separate_occurrences_by_consensus_kmer(all_occurrence_filepath: Path, output_folder_path: Path):
    """
    function to split the large occurrences file of all k-mer occurrences into separate occurrences.
    The instances for each consensus k-mer is saved as sharkcapture_{consensus_kmer}_occurrences.tsv in the output folder.

    :param (Path) all_occurrence_filepath: file path to all occurrences file
    :param (Path) output_folder_path: path to output folder

    :return: None
    """
    occs = pd.read_csv(all_occurrence_filepath, sep="\t")
    for ref_kmer, frame in occs.groupby('reference_kmer'):
        out_frame_name = output_folder_path / f"sharkcapture_{ref_kmer}_occurrences.tsv"
        frame.to_csv(out_frame_name, sep="\t", index=False)
        print(f'output {ref_kmer} matches to {out_frame_name}')

    return None