import os
import shutil
import json
import argparse

from ...core.utils import read_fasta_file
from ...core.utils import form_sequence_pairs


def generate_input_files(sequence_fasta_file_path, k_max, input_data_dir, proceed_force_flag=False):
    """
    Read the fasta file of set of sequences which need to be studied for conservation,
    and create separate master input files for pair-wise computation
    If, k_max = 10; Then 8 files - k_3.json, k_4.json, .., k_10.json are created

    :param(str) sequence_fasta_file_path: Fasta file of input set of sequences
    :param(int) k_max: Max K-Mer length; Separate files created for 3 to this value
    :param(str) input_data_dir: Folder path where all input param files need to be stored
    :param(bool) proceed_force_flag: Should force proceed or not in case of k > sequence length
    """
    id_seq_map = read_fasta_file(file_path=sequence_fasta_file_path)
    min_seq_len = min([len(sequence) for sequence in id_seq_map.values()])
    if k_max > min_seq_len:
        print("\nAt least one sequence with length ({}) smaller than 'k_max' ({}) !!".format(min_seq_len, k_max))
        if proceed_force_flag:
            print("[Force flagged] Proceeding with current set of sequences and k_max = {}".format(k_max))
        else:
            print("\nOptions:\n1. Restart script with new inputs (fasta file and/or k_max)"
                  "\n2. Set k_max to shortest sequence's length ({})"
                  "\n3. Proceed Anyway".format(min_seq_len))
            user_input = int(input('Enter 1, 2, or 3: '))
            if user_input == 1:
                exit('Exiting... Restart with new input fasta file or k_max')
            elif user_input == 2:
                print("Setting 'k_max' = {}".format(min_seq_len))
                k_max = min_seq_len
            else:
                print("Proceeding with current set of sequences and k_max = {}".format(k_max))
    pair_id__input_param_map = form_sequence_pairs(id_seq_map)
    print("No. of computation units (sequence pairs): {}".format(len(pair_id__input_param_map)))
    if os.path.exists(input_data_dir):
        print("Purging existing {}".format(input_data_dir))
        shutil.rmtree(input_data_dir, ignore_errors=True)
    os.makedirs(input_data_dir)
    for k in range(3, k_max + 1):
        file_data = {
            'k': k,
            'input_params': list(pair_id__input_param_map.values())
        }
        file_path = "{}/k_{}.json".format(input_data_dir, k)
        with open(file=file_path, mode='w') as json_file:
            json.dump(file_data, json_file)
        print("k={} - Created master input data file at {}".format(k, file_path))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CAPTURE: Prepare master data input files for reciprocal processing. '
                                                 'Each k has a separate json file to facilitate parallel processing')
    parser.add_argument('k_max', help='Max length of k-mer', type=int)
    parser.add_argument('fasta_file_path', help='Absolute path to master file of sequences in fasta format', type=str)
    parser.add_argument('out_dir', help='Absolute path to folder to store files per k', type=str)
    parser.add_argument('-f', '--force', help='Force proceed in case of sequence shorter than k', action='store_true')
    args = parser.parse_args()
    generate_input_files(sequence_fasta_file_path=args.fasta_file_path, k_max=args.k_max, input_data_dir=args.out_dir,
                         proceed_force_flag=args.force)
