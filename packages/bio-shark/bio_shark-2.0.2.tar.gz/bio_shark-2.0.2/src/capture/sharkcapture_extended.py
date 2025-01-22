import os.path
import pandas as pd
from pathlib import Path
from typing import Iterable, Tuple, Iterator
import os

def is_overlap(start_1, end_1, start_2, end_2):
    """
    Checks if two sequences are overlapping with each other.

    :param (int) start_1: start amino acid coordinate of the first sequence
    :param (int) end_1: end amino acid coordinate of the first sequence
    :param (int) start_2: start amino acid coordinate of the second sequence
    :param (int) end_2: end amino acid coordinate of the second sequence

    :return (bool): True if two sequences are overlapping with each other, False otherwise
    """
    if start_1 in range(start_2, end_2+1) or end_1 in range(start_2, end_2+1) or start_2 in range(start_1, end_1+1) or end_2 in range(start_1, end_1+1):
        return True
    else:
        return False

def overlaps(ranges: Iterable[Tuple[int, int]]) -> Iterable[Tuple[int, int]]:
    """
    Identifies and concatenates ranges that overlap with each other.
    :param ranges: list of tuples (start,end)
    :return: list of tuples (start,end) where overlapping ranges are concatenated into one long range
    """
    ranges = sorted(ranges)  # If our inputs are guaranteed sorted, we can skip this
    it: Iterator = iter(ranges)
    try:
        curr_start, curr_stop = next(it)
    except StopIteration:
        return
    for start, stop in it:
        if curr_start <= start <= curr_stop:  # Assumes intervals are closed
            curr_stop = max(curr_stop, stop)
        else:
            yield curr_start, curr_stop
            curr_start, curr_stop = start, stop
    yield curr_start, curr_stop


def collapse_to_core_kmers(full_df: pd.DataFrame, score_cutoff_prop: float = 0.90, save: bool = True,
                           outfile_path: Path = None, simplified: bool = False):

    """
    performs k-mer extension based on a score cutoff percentage

    :param (pd.DataFrame) full_df: dataframe containing all kmer occurrences and their shark-capture scores,
    across all sequences
    :param (float) score_cutoff_prop: cutoff proportion of sharkcapture score to consider a k-mer for extension
    (default 0.90). Only k-mer matches above score_cutoff_prop * highest shark-capture score will be considered.
    :param (bool) save: whether to save the output file (default True)
    :param (Path) outfile_path: path to output file (optional). If not given and save=True, output file will be saved as
    input file+merged.collapsed.tsv
    :param (bool) simplified: whether to remove information on the k-mer before extension, e.g. original start and end
     positions, original matched sequence (default False)

    :return (pd.DataFrame) df_result: resulting dataframe containing all k-mer occurrences and their shark-capture
    scores following the extension protocol
    """

    df_result=pd.DataFrame()

    full_df['to_collapse'] = False

    #GET ORDER OF REFERENCE_KMERS
    order=list(dict.fromkeys(list(full_df['reference_kmer'])))
    order_dict={kmer:index+1 for index,kmer in enumerate(order)}
    # FOR EACH UNIQUE K-MER, GIVE THEN A 'RANK' FOR SORTING
    full_df['rank'] = full_df.apply(lambda row: order_dict[row['reference_kmer']], axis=1)

    for seqid, df in full_df.groupby('sequenceID'):
        # MAINTAIN ORDER OF REFERENCE K-MERS ACCORDING TO ORIGINAL SCOREFILE, AND SORT ACCORDING TO START
        df=df.sort_values(by=['rank','start'], ascending=[True,True])
        if not df.sharkcapture_score.is_monotonic_decreasing:
            raise Exception('this is super weird')
        df.reset_index(drop=True,inplace=True)
        ls = []
        for i, row_i in df.iterrows():
            if df.iloc[i, df.columns.get_loc('to_collapse')]:
                continue
            start_i, end_i = row_i['start'], row_i['end']
            core_start, core_end = row_i['start'], row_i['end']
            max_score = row_i['sharkcapture_score']

            #FILTER FOR MATCHES IN ACCEPTABLE SCORE RANGE
            acceptable_score = max_score * score_cutoff_prop
            collapsible_df = df[(df['sharkcapture_score']>=acceptable_score) & (df['to_collapse']==False)]

            # TRACK THE AMINO ACID CORRESPONDING TO EACH POSITION
            sequence_coordinate_map = {}
            for match, start, end in list(zip(collapsible_df['match'], collapsible_df['start'], collapsible_df['end'])):
                aa_positions = list(range(int(start), int(end+1)))
                match = list(match)
                if len(match)!=len(aa_positions):
                    raise Exception('length of match does not match number of amino acids')
                else:
                    sequence_coordinate_map.update(dict(zip(aa_positions, match)))

            # IDENTIFY CONSECUTIVE AMINO ACID STRETCHES WITHIN ACCEPTABLE SCORE RANGE. This requires overlap between matches.
            collapsed_range = overlaps(zip(collapsible_df['start'], collapsible_df['end']))

            final = []
            for start, end in collapsed_range:
                if is_overlap(start, end, start_i, end_i):
                    final.append((start, end))
            if len(final)!=1:
                raise Exception('there should only be one region that contains the k-mer')
            else:
                final = final[0]
            for index, row in collapsible_df.iterrows():
                if is_overlap(row['start'],row['end'],final[0],final[1]):
                    df.at[index, 'to_collapse'] = True #SKIP OVER THESE ROWS FROM NOW ON
            row_i['extended_start'] = final[0]
            row_i['extended_end'] = final[1]
            extended_seq = ''.join([sequence_coordinate_map[x] for x in range(final[0], final[1]+1)])
            row_i['extended_seq'] = extended_seq
            row_i['start'] = core_start
            row_i['end'] = core_end
            ls.append(row_i)

        df_result_perseq = pd.concat(ls, axis=1).transpose()
        df_result_perseq.reset_index(inplace=True, drop=True)
        if not df_result_perseq.sharkcapture_score.is_monotonic_decreasing:
            raise Exception('scores should be monotonically decreasing')
        df_result_perseq['overlap_check'] = False
        segments = list(zip(df_result_perseq.index,df_result_perseq['extended_start'],df_result_perseq['extended_end']))
        for index, row in df_result_perseq.iterrows():
            if row['overlap_check']:
                continue
            for row_index, start, end in segments[index+1:]:
                if is_overlap(start, end, row['extended_start'], row['extended_end']):
                    df_result_perseq.at[row_index, 'overlap_check'] = True
        df_result_perseq = df_result_perseq[~df_result_perseq['overlap_check']]
        df_result_perseq.reset_index(inplace=True, drop=True)
        df_result=pd.concat([df_result, df_result_perseq])
        if not df_result_perseq.sharkcapture_score.is_monotonic_decreasing:
            raise Exception('scores should be monotonically decreasing')

    df_result.reset_index(drop=True, inplace=True)

    #simplify results by only keeping the extended matches
    if simplified:
        df_result = df_result.loc[:, ['sequenceID', 'reference_kmer','sharkcapture_score','extended_start', 'extended_end', 'extended_seq']]
        df_result = df_result.rename(columns={'extended_start': 'start', 'extended_end': 'end', 'extended_seq': 'match'})

    #save result if necessary
    if save:
        if outfile_path:
            df_result.to_csv(outfile_path, sep='\t', index=False)
        else:
            kmer_occurrence_filepath= Path(os.getcwd())
            df_result.to_csv(kmer_occurrence_filepath / 'kmers_extended_occurrences.tsv', sep='\t', index=False)

    return df_result