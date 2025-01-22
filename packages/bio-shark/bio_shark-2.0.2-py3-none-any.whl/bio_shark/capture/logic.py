from typing import Mapping, Tuple, List
from ..core.sequence_pair_similarity import SeqPairSimilarity


TYPE_SCORE_MATRIX = Mapping[str, Mapping[str, float]]


def get_hadamard_matrix(sequence1: str, sequence2: str, k: int,
                        substitution_matrix: Tuple[TYPE_SCORE_MATRIX, float, float]) -> TYPE_SCORE_MATRIX:
    """
    Compute the reciprocal and hadamard matrix for two sequences using the sequence score's similarity logic

    :param(str) sequence1: First protein sequence
    :param(str) sequence2: Second protein sequence
    :param(int) k: K-Mer length (should be between 3 and 10)
    :param(dict[str, dict[str, float]], float, float) substitution_matrix: Subs matrix table, Max score, Min score
    :return(dict of dict): The hadamard product of similarity and reciprocal matrix
    """
    seq_pair_score = SeqPairSimilarity(
        k=k,
        sequence1=sequence1,
        sequence2=sequence2,
        substitution_matrix=substitution_matrix
    )
    seq_pair_score.compute_kmer_maps()
    seq_pair_score.generate_similarity_matrix()
    reciprocal_matrix, hadamard_matrix = seq_pair_score.generate_reciprocal_matrix()
    return hadamard_matrix


def get_all_kmers(hadamard_matrices: List[TYPE_SCORE_MATRIX], is_score_weighted: bool = True) -> Mapping[str, float]:
    """
    Use the hadamard matrices (reciprocal (.) similarity) from a set of sequence pair comparisons
        and chalk out list of unique k-mers and score as per count/weight
        Prints sorted list of k-mers in descending order of score

    :param(bool) is_score_weighted: Increment by score if True (weighted) else 1 (count)
    :param(list of dict of dict) hadamard_matrices:
    :return(dict[str, float]): Top K-mers selected after sorting the output list
    """

    def _increment_super_matrix(kmer_outer: str, kmer_inner: str, super_matrix_ref: TYPE_SCORE_MATRIX,
                                increment: float):
        """Modular function to repeat the same task for the inversed position"""
        if kmer_outer not in super_matrix_ref:
            super_matrix_ref[kmer_outer] = {kmer_inner: increment}
        else:
            if kmer_inner not in super_matrix_ref[kmer_outer]:
                super_matrix_ref[kmer_outer][kmer_inner] = increment
            else:
                super_matrix_ref[kmer_outer][kmer_inner] += increment

    super_matrix = {}
    for hadamard_matrix in hadamard_matrices:
        for kmer1, kmer1_scores in hadamard_matrix.items():
            for kmer2, score in kmer1_scores.items():
                score = score if is_score_weighted else 1
                _increment_super_matrix(kmer1, kmer2, super_matrix, score)
                if kmer1 != kmer2:
                    _increment_super_matrix(kmer2, kmer1, super_matrix, score)

    print("Search space (no. unique k-mers): {}".format(len(super_matrix)))
    kmer_final_score_map = {kmer: sum(kmer_scores.values()) for kmer, kmer_scores in super_matrix.items()}
    sorted_kmer_score_map = dict(sorted(kmer_final_score_map.items(), key=lambda item: item[1], reverse=True))

    return sorted_kmer_score_map


