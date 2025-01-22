import os

here = os.path.abspath(os.path.dirname(__file__))

DATA_DIR = os.path.join(here, 'data')
SUBS_MATRIX_DIR = os.path.join(DATA_DIR, 'substitution_matrix_grantham.tsv')
DIVE_MODEL_PKL_PATH = os.path.join(DATA_DIR, 'dive_pred_model_v2.pkl')
VISUALISATION_PKL_PATH = os.path.join(DATA_DIR, 'SHARKdive_features_boxplot_stats_NGDinvert.pkl')

ROUND_OFF_DP = 10

MASKING_CHARACTER = '*'

CANONICAL_AAS = 'ARNDCQEGHILKMFPSTWYV' + MASKING_CHARACTER
