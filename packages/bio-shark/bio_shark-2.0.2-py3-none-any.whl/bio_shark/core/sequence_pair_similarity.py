import math
from typing import Mapping, Tuple, List

TYPE_SCORE_MATRIX = Mapping[str, Mapping[str, float]]


class SeqPairSimilarity:
    def __init__(self, sequence1: str,
                 sequence2: str, k: int,
                 substitution_matrix: Tuple[TYPE_SCORE_MATRIX, float, float]):
        """
        :param(str) sequence1: First Sequence
        :param(str) sequence2: Second Sequence
        :param(int) k: Length of k-mer
        :param(dict[str, dict[str, float]], float, float) substitution_matrix: Subs matrix table, Max score, Min score
        """
        self.sequence1 = sequence1
        self.sequence2 = sequence2
        self.k = k
        if len(self.sequence1) < self.k or len(self.sequence2) < self.k:
            print('Sequence 1 Length: {}; Sequence 2 Length: {}; K = {}'.format(
                len(self.sequence1), len(self.sequence2), self.k))
            raise Exception('K-Mer length should not be greater than sequence length')
        self.substitution_matrix_obj = substitution_matrix
        self.kmer_count_map_1 = {}
        self.kmer_count_map_2 = {}
        self.similarity_matrix = {}

    @staticmethod
    def get_length_difference(a: float, b: float) -> float:
        """
        Length Difference function, often used for tie-breakers

        :param(float) a: Count 1
        :param(float) b: Count 2
        :return(float): Length Difference
        """
        numerator_sq = 2 * (a * a + b * b)
        return math.sqrt(numerator_sq) / (a + b)

    @staticmethod
    def generate_kmer_map(sequence: str, k_value: int) -> Mapping[str, int]:
        """
        For a given sequence and size of k-mer, count the occurrences of all possible k-mers

        :param(str) sequence: Given sequence
        :param(int) k_value: Given k-value / Length of k-mer
        :return(dict[str, int]): Key -> K-Mer; Value -> Count in respective sequence
        """
        kmer_count_map = {}
        for i in range(len(sequence) - k_value + 1):
            kmer = sequence[i: i + k_value]
            # residues can be masked with the '*' character. K-mers that contain masked residues should be ignored
            if '*' in kmer:
                continue
            elif kmer in kmer_count_map:
                kmer_count_map[kmer] += 1
            else:
                kmer_count_map[kmer] = 1
        return kmer_count_map

    @staticmethod
    def get_kmer_similarity_score(kmer1: str, kmer2: str,
                                  substitution_matrix: Tuple[TYPE_SCORE_MATRIX, float, float]) -> float:
        """
        For two given k-mers of same size, compute the similarity score b/w them using a substitution matrix
        Score is normalised to be between 0 and 1

        :param(dict[str, dict[str, float]], float, float) substitution_matrix: Subs matrix table, Max score, Min score
        :param(str) kmer1: First k-mer
        :param(str) kmer2: Second k-mer
        :return(float): Similarity score
        """
        subs_matr, subs_max, subs_min = substitution_matrix
        kmer_len = len(kmer1)
        if kmer_len != len(kmer2):
            raise Exception('K-Mer lengths should be same')

        score_sum = 0
        for i in range(kmer_len):
            try:
                d_score = 1 - ((subs_matr[kmer1[i]][kmer2[i]] - subs_min) / (subs_max - subs_min))
            except KeyError:
                print('ERROR: An amino acid of either {} or {} is not present in substitution matrix'.format(kmer1,
                                                                                                             kmer2))
                d_score = 0
                # Or we can also abort from here
            score_sum += d_score
        return score_sum / kmer_len

    @staticmethod
    def get_axis_score(axis1_kmer_count_map: Mapping[str, int],
                       axis2_kmer_count_map: Mapping[str, int],
                       similarity_matrix: TYPE_SCORE_MATRIX,
                       reverse=False, is_ld_needed=True) -> list:
        """
        A common function to iterate row-wise and column-wise over the similarity matrix and compute sums

        :param(boolean) is_ld_needed: Flag to indicate if length difference should be used for tie-breaker
        :param(dict[str, int]) axis1_kmer_count_map: Mapping of each k-mer count of protein in first position
        :param(dict[str, int]) axis2_kmer_count_map: Mapping of each k-mer count of protein in second position
        :param(dict[str, dict[str, float]]) similarity_matrix: Matrix to represent similarity of k-mers
            Similar to the class variable self.similarity_matrix (output of function generate_similarity_matrix())
        :param(bool) reverse: If matrix access needs to be reversed (True for columns)
        :return(list): Summed score
        """
        axis_scores = []
        for kmer_seq1, count_kmer_seq1 in axis1_kmer_count_map.items():
            deno = 0
            num_sum = 0
            for kmer_seq2, count_kmer_seq2 in axis2_kmer_count_map.items():
                if not reverse:
                    cell_value = similarity_matrix[kmer_seq1][kmer_seq2]
                else:
                    cell_value = similarity_matrix[kmer_seq2][kmer_seq1]
                if cell_value < 0:
                    continue
                deno += count_kmer_seq2
                num_sum += count_kmer_seq2 * cell_value
            if deno != 0:
                axis_score = count_kmer_seq1 * num_sum / deno
                if is_ld_needed:
                    ld_factor = SeqPairSimilarity.get_length_difference(count_kmer_seq1, deno)
                    axis_score = axis_score / ld_factor
            else:
                axis_score = 0
            axis_scores.append(axis_score)
        return axis_scores

    @staticmethod
    def max_value_indexes(axis1_kmer_count_map: Mapping[str, int],
                          axis2_kmer_count_map: Mapping[str, int],
                          similarity_matrix: TYPE_SCORE_MATRIX,
                          reverse=False) -> List[Tuple[str, str]]:
        """
        Parse the similarity matrix row/column-wise and return the list of indexes with max value

        :param(dict[str, int]) axis1_kmer_count_map: Mapping of each k-mer count of protein in first position
        :param(dict[str, int]) axis2_kmer_count_map: Mapping of each k-mer count of protein in second position
        :param(dict[str, dict[str, float]]) similarity_matrix: Matrix to represent similarity of k-mers
            Similar to the class variable self.similarity_matrix (output of function generate_similarity_matrix())
        :param(bool) reverse: If matrix access needs to be reversed (True for columns)
        :return(list of tuples[str, str]): Each tuple points to one cell in the similarity matrix with the index k_mers
        """
        retained_kmers = []
        for kmer_seq1, count_kmer_seq1 in axis1_kmer_count_map.items():
            max_value = -1
            max_value_idxs = ()
            prev_ld_score = -1
            for kmer_seq2, count_kmer_seq2 in axis2_kmer_count_map.items():
                max_flag = False
                if not reverse:
                    cell_value = similarity_matrix[kmer_seq1][kmer_seq2]
                else:
                    cell_value = similarity_matrix[kmer_seq2][kmer_seq1]
                if cell_value > max_value:
                    max_flag = True
                if cell_value == max_value:
                    ld_score = SeqPairSimilarity.get_length_difference(count_kmer_seq1, count_kmer_seq2)
                    if ld_score < prev_ld_score:
                        max_flag = True
                if max_flag:
                    max_value = cell_value
                    max_value_idxs = (kmer_seq1, kmer_seq2) if not reverse else (kmer_seq2, kmer_seq1)
                    prev_ld_score = SeqPairSimilarity.get_length_difference(count_kmer_seq1, count_kmer_seq2)
            retained_kmers.append(max_value_idxs)
        return retained_kmers

    def generate_similarity_matrix(self):
        """
        Generate the similarity matrix in a dict of dict format
        Outer-map: Keys -> k-mers of the first sequence; Value -> Inner-map
        Inner-map: Keys -> K-mers of the second sequence; Value -> Similarity score
        """
        for kmer_seq1 in self.kmer_count_map_1.keys():
            similarity_matrix_row = {}
            for kmer_seq2 in self.kmer_count_map_2.keys():
                score = self.get_kmer_similarity_score(kmer_seq1, kmer_seq2, self.substitution_matrix_obj)
                similarity_matrix_row[kmer_seq2] = score
            self.similarity_matrix[kmer_seq1] = similarity_matrix_row

    def compute_kmer_maps(self):
        """
        Compute kmer-count hashmap for both the sequences
        """
        self.kmer_count_map_1 = self.generate_kmer_map(sequence=self.sequence1, k_value=self.k)
        self.kmer_count_map_2 = self.generate_kmer_map(sequence=self.sequence2, k_value=self.k)

    def filter_similarity_matrix(self, threshold: float):
        """
        Normal static threshold filtering
        """
        for kmer_seq1 in self.kmer_count_map_1.keys():
            for kmer_seq2 in self.kmer_count_map_2.keys():
                if self.similarity_matrix[kmer_seq1][kmer_seq2] <= threshold:
                    self.similarity_matrix[kmer_seq1][kmer_seq2] = -1

    def filter_similarity_matrix__sparse(self) -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]]]:
        """
        Only retain the cells if they are the max in either their own row or column
        """
        retained_indexes_rows = self.max_value_indexes(self.kmer_count_map_1, self.kmer_count_map_2,
                                                       self.similarity_matrix)
        retained_indexes_cols = self.max_value_indexes(self.kmer_count_map_2, self.kmer_count_map_1,
                                                       self.similarity_matrix, reverse=True)
        retained_indexes = retained_indexes_rows + retained_indexes_cols
        for kmer_seq1 in self.kmer_count_map_1.keys():
            for kmer_seq2 in self.kmer_count_map_2.keys():
                if (kmer_seq1, kmer_seq2) in retained_indexes:
                    continue
                self.similarity_matrix[kmer_seq1][kmer_seq2] = -1
        # M_dashed = self.similarity_matrix at this point
        return retained_indexes_rows, retained_indexes_cols

    def get_similarity_score(self, threshold: float) -> float:
        """
        Get similarity score (variant: normal)

        :param(float) threshold: Threshold for normal filtering
        :return(float): Normal Similarity Score
        """
        if not (self.kmer_count_map_1 and self.kmer_count_map_2 and self.similarity_matrix):
            raise Exception('Compute pre-requisites')
        self.filter_similarity_matrix(threshold)
        row_scores = self.get_axis_score(self.kmer_count_map_1, self.kmer_count_map_2, self.similarity_matrix)
        column_scores = self.get_axis_score(self.kmer_count_map_2, self.kmer_count_map_1, self.similarity_matrix,
                                            reverse=True)
        final_score = (sum(row_scores) + sum(column_scores)) / (
                sum(self.kmer_count_map_1.values()) + sum(self.kmer_count_map_2.values()))
        return final_score

    def get_similarity_score__sparse(self) -> float:
        """
        Get similarity score (variant: sparse)

        :return(float): Sparse Score
        """
        if not (self.kmer_count_map_1 and self.kmer_count_map_2 and self.similarity_matrix):
            raise Exception('Compute pre-requisites')
        self.filter_similarity_matrix__sparse()
        sparse_score = 0
        norm_factor = 0
        for kmer_seq1, count_kmer_seq1 in self.kmer_count_map_1.items():
            for kmer_seq2, count_kmer_seq2 in self.kmer_count_map_2.items():
                cell_value = self.similarity_matrix[kmer_seq1][kmer_seq2]
                if cell_value > -1:
                    norm_factor += (count_kmer_seq1 * count_kmer_seq2)
                    sparse_score += (count_kmer_seq1 * count_kmer_seq2 * cell_value) / self.get_length_difference(
                        count_kmer_seq1, count_kmer_seq2)
        if norm_factor == 0:
            return 0
        final_sparse_score = sparse_score / norm_factor
        return final_sparse_score

    def get_similarity_score__collapsed(self) -> float:
        """
        Get similarity score (variant: collapsed)

        :return(float): Collapsed Score
        """
        if not (self.kmer_count_map_1 and self.kmer_count_map_2 and self.similarity_matrix):
            raise Exception('Compute pre-requisites')
        self.filter_similarity_matrix__sparse()
        row_scores = self.get_axis_score(self.kmer_count_map_1, self.kmer_count_map_2, self.similarity_matrix,
                                         is_ld_needed=False)
        column_scores = self.get_axis_score(self.kmer_count_map_2, self.kmer_count_map_1,
                                            self.similarity_matrix, reverse=True, is_ld_needed=False)
        final_score = (sum(row_scores) + sum(column_scores)) / (
                len(self.sequence1) + len(self.sequence2) - 2 * (self.k - 1))
        return final_score

    def generate_reciprocal_matrix(self) -> Tuple[TYPE_SCORE_MATRIX, TYPE_SCORE_MATRIX]:
        """
        :return(dict[str, dict[str, float]], dict[str, dict[str, float]]): Reciprocal matrix,
            its hadamard product with the similarity matrix
        """
        if not (self.kmer_count_map_1 and self.kmer_count_map_2 and self.similarity_matrix):
            raise Exception('Compute pre-requisites')
        reciprocal_matrix = {}
        hadamard_matrix = {}  # C = M (.) R
        retained_indexes_rows, retained_indexes_cols = self.filter_similarity_matrix__sparse()
        for kmer_seq1 in self.kmer_count_map_1.keys():
            reciprocal_matrix_row = {}
            hadamard_matrix_row = {}
            for kmer_seq2 in self.kmer_count_map_2.keys():
                if not ((kmer_seq1, kmer_seq2) in retained_indexes_rows and
                        (kmer_seq1, kmer_seq2) in retained_indexes_cols):
                    continue  # r_val = 0; so this entry be ignored
                r_val = 1
                reciprocal_matrix_row[kmer_seq2] = r_val
                hadamard_matrix_row[kmer_seq2] = self.similarity_matrix[kmer_seq1][kmer_seq2] * r_val
            if reciprocal_matrix_row or hadamard_matrix_row:
                reciprocal_matrix[kmer_seq1] = reciprocal_matrix_row
                hadamard_matrix[kmer_seq1] = hadamard_matrix_row
        return reciprocal_matrix, hadamard_matrix
