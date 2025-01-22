import csv
import math
from typing import Mapping, Tuple, Union
from pathlib import Path

from .. import settings
from ..exceptions import DuplicateSequenceIdError

TYPE_SCORE_MATRIX = Mapping[str, Mapping[str, float]]


def load_subs_matrix(file_url: str) -> Tuple[TYPE_SCORE_MATRIX, float, float]:
    """
    Read a substitution matrix tsv/csv file present in tabular format and return it in dictionary format

    :param(str) file_url: Tab-separated file path for the substitution matrix file
    :return(dict[str, dict[str, float]], float, float): The substitution matrix in dict of dict form.
        The outer dict has keys as amino acids and values as a dict of scores for other amino acids
        Second and third values are min and max scores from the table
    """
    subs_matrix = {}
    all_aas = []
    matrix_min = math.inf
    matrix_max = 0
    with open(file=file_url, mode='r', newline='') as csvfile:
        for row in csv.reader(csvfile, delimiter='\t'):
            if row[0] == '.':
                all_aas = row[1:]
                continue
            subs_matrix_aa = {}
            for i in range(len(all_aas)):
                cell_score = int(row[i + 1])
                matrix_min = cell_score if cell_score < matrix_min else matrix_min
                matrix_max = cell_score if cell_score > matrix_max else matrix_max
                subs_matrix_aa[all_aas[i]] = cell_score
            subs_matrix[row[0]] = subs_matrix_aa
    return subs_matrix, matrix_max, matrix_min


def get_grantham_subs_matrix() -> Tuple[TYPE_SCORE_MATRIX, float, float]:
    """Load a specific substitution matrix from the given file path"""
    return load_subs_matrix(file_url=settings.SUBS_MATRIX_DIR)


def read_fasta_file(file_path: Union[str, Path]) -> Mapping[str, str]:
    """
    Read a sequence fasta file and prepare a hash-map with ID and sequence
    Also accounts for a fasta file where a same sequence has line-breaks in between

    :param(str) file_path: URL of fasta file for sequences
    :return(dict[str, str]): Key -> Sequence ID; Value: Sequence
    """
    id_seq_map = {}
    skip_count = 0

    def _insert_map(sequence_id: str,
                    sequence: str,
                    _id_seq_map: Mapping[str, str],
                    _skip_count: int) -> Tuple[Mapping[str, str], int]:
        if sequence_id and sequence:
            has_non_cano_aa = False
            for aa in sequence:
                if aa not in settings.CANONICAL_AAS:
                    has_non_cano_aa = True
                    break
            if sequence_id in _id_seq_map:
                raise DuplicateSequenceIdError(seq_id=sequence_id)
            if not has_non_cano_aa:
                _id_seq_map[sequence_id] = sequence
            else:
                _skip_count += 1
        return _id_seq_map, _skip_count

    curr_id = None
    curr_sequence = ''
    with open(file=file_path) as fasta_file:
        for line in fasta_file.readlines():
            if line.startswith('>'):
                # Map existing sequence to ID; This line has next ID
                id_seq_map, skip_count = _insert_map(curr_id, curr_sequence, id_seq_map, skip_count)
                curr_id = line[1:].strip()
                curr_sequence = ''
                continue
            if curr_id and not line.startswith('>'):
                curr_sequence = curr_sequence.strip() + line.strip()

    id_seq_map, skip_count = _insert_map(curr_id, curr_sequence, id_seq_map, skip_count)

    print("Read fasta file from path {}; Found {} sequences; Skipped {} sequences for having non-canonical AAs".
          format(file_path, len(id_seq_map), skip_count))
    return id_seq_map


def form_sequence_pairs(id_seq_map: Mapping[str, str],
                        id_seq_map2: Mapping[str, str] = None
                        ) -> Mapping[str, Mapping[str, str]]:
    """
    Generate unique sequence pairs from one / two list of sequences
    For one list, compute intra-group pairs and inter-group for two.

    :param (dict[str, str]) id_seq_map: Mapping of sequence with fasta ID. Key -> Fasta ID; Value -> Fasta Sequence
    :param (dict[str, str]) id_seq_map2: Mapping of sequence with fasta ID. Key -> Fasta ID; Value -> Fasta Sequence
    :return (dict[str, dict[str, str]]): Key -> Unique Sequence Pair ID (concatenated);
        Value -> Dictionary with 'seq_id1', 'seq_id2', 'sequence1', 'sequence2'
    """
    pair_id__input_param_map = {}  # Logic: Unique sequence pairs (not all pairs)
    # In the above dict, key is a unique identifier for the pair
    id_seq_map2 = id_seq_map2 if id_seq_map2 else id_seq_map
    for seq_id1, sequence1 in id_seq_map.items():
        for seq_id2, sequence2 in id_seq_map2.items():
            pair_id = '__'.join(sorted([seq_id1, seq_id2]))
            if pair_id in pair_id__input_param_map:
                continue
            pair_id__input_param_map[pair_id] = {
                'seq_id1': seq_id1,
                'seq_id2': seq_id2,
                'sequence1': sequence1,
                'sequence2': sequence2
            }
    return pair_id__input_param_map
