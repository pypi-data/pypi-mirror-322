from enum import Enum

"""
Create folder structure
"""
SUBDIR_INPUT = 'inputs'
SUBDIR_INTERMEDIATES = 'intermediates'
SUBDIR_OUTPUT = 'outputs'
SUBDIR_PLOTS = SUBDIR_OUTPUT + '/' + "plots"

SUBDIR_CONSERVED_KMERS = SUBDIR_INTERMEDIATES + '/' + "conserved_kmers"
SUBDIR_HADAMARDS = SUBDIR_INTERMEDIATES + '/' + 'hadamards'

SUBDIR_OCCURRENCES = SUBDIR_OUTPUT + '/' + "occurrences"

SUBDIR_LOGOS = SUBDIR_PLOTS + '/' + "logos"
SUBDIR_PER_SEQUENCE_MATCHES = SUBDIR_PLOTS + '/' + "per_sequence_matches"

class FileNames(Enum):
    ALL_HADAMARDS_JSON_FILE = "all_hadamards.json_all"
    ALL_OCCURRENCES_TSV_FILE = "all_occurrences.tsv"
    ALL_OCCURRENCES_EXTENDED_TSV_FILE = "all_occurrences_extended.tsv"

