from ..core.sequence_pair_similarity import SeqPairSimilarity
from ..core import utils
from .. import settings

substitution_matrix_obj = utils.get_grantham_subs_matrix()


def run_normal(sequence1: str, sequence2: str, k: int, threshold: float) -> float:
    """
    Compute similarity score (vanilla/complete-collapsed version)

    :param(float) threshold: Dive-normal threshold (user input)
    :param(str) sequence1: First protein sequence
    :param(str) sequence2: Second protein sequence
    :param(int) k: K-Mer length
    :return(float): Normal Similarity score
    """
    seq_pair_score = SeqPairSimilarity(
        k=k,
        sequence1=sequence1,
        sequence2=sequence2,
        substitution_matrix=substitution_matrix_obj
    )
    seq_pair_score.compute_kmer_maps()
    seq_pair_score.generate_similarity_matrix()
    final_score = round(seq_pair_score.get_similarity_score(threshold), settings.ROUND_OFF_DP)
    return final_score


def run_sparse(sequence1: str, sequence2: str, k: int) -> float:
    """
    Compute similarity score (sparse version)

    :param(str) sequence1: First protein sequence
    :param(str) sequence2: Second protein sequence
    :param(int) k: K-Mer length
    :return(float): Sparse Similarity score
    """
    seq_pair_score = SeqPairSimilarity(
        k=k,
        sequence1=sequence1,
        sequence2=sequence2,
        substitution_matrix=substitution_matrix_obj
    )
    seq_pair_score.compute_kmer_maps()
    seq_pair_score.generate_similarity_matrix()
    final_score = round(seq_pair_score.get_similarity_score__sparse(), settings.ROUND_OFF_DP)
    return final_score


def run_collapsed(sequence1: str, sequence2: str, k: int) -> float:
    """
    Compute similarity score (collapsed version)

    :param(str) sequence1: First protein sequence
    :param(str) sequence2: Second protein sequence
    :param(int) k: K-Mer length
    :return(float): Collapsed Similarity score
    """
    seq_pair_score = SeqPairSimilarity(
        k=k,
        sequence1=sequence1,
        sequence2=sequence2,
        substitution_matrix=substitution_matrix_obj
    )
    seq_pair_score.compute_kmer_maps()
    seq_pair_score.generate_similarity_matrix()
    final_score = round(seq_pair_score.get_similarity_score__collapsed(), settings.ROUND_OFF_DP)
    return final_score


def user_run():
    """Driver function for user to try out shark-dive scoring"""
    ip_seq1 = input('Enter Sequence 1:\n').strip()
    ip_seq2 = input('Enter Sequence 2:\n').strip()
    k_mer_len = int(input('Enter k-mer length (integer 1 - 10): '))
    variant_choice = int(input('Press: 1. Normal; 2. Sparse\n'))
    normal_threshold = None
    if variant_choice == 1:
        run_fn = run_normal
        normal_threshold = float(input('Enter threshold: \n'))
    elif variant_choice == 2:
        run_fn = run_sparse
    else:
        exit('Variant choices available are only 1 or 2')
    run_param_args = {
        'sequence1': ip_seq1,
        'sequence2': ip_seq2,
        'k': k_mer_len,
    }
    if variant_choice == 1:
        run_param_args['threshold'] = normal_threshold
    result = run_fn(**run_param_args)
    print("Similarity Score: {}".format(result))


if __name__ == '__main__':
    user_run()
