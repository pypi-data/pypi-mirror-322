from .. import settings

from alfpy.utils.seqrecords import SeqRecords
from alfpy import word_distance
from alfpy import word_pattern
from alfpy import word_vector

ALLOWED_K_MAX = 6


def get_google_distance_score(sequence1: str, sequence2: str, k: int) -> float:
    """
    For two sequences, compute the Google distance similarity score

    :param(str) sequence1: Sequence 1
    :param(str) sequence2: Sequence 2
    :param(int) k: K-Mer length
    :return(float): Similarity Score
    """
    if k >= ALLOWED_K_MAX:
        print("Alf Google Distance score can only be computed for k < {}".format(ALLOWED_K_MAX))
        return

    seq_records = SeqRecords()
    seq_records.add('seq1', sequence1)
    seq_records.add('seq2', sequence2)

    pattern = word_pattern.create(seq_records.seq_list, word_size=k)
    counts = word_vector.Counts(seq_records.length_list, pattern)
    dist = word_distance.Distance(counts, 'google')
    score = dist.pairwise_distance(0, 1)
    rounded_score = round(score, settings.ROUND_OFF_DP)
    return rounded_score
