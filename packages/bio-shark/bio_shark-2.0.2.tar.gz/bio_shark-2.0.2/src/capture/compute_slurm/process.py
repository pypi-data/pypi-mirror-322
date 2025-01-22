"""To be run in parallel using SLURM"""

import datetime
import os
import json
import argparse
import time


from ...core import utils
from ..logic import get_hadamard_matrix


def process(input_data_file_path, chunk_size, output_data_dir):
    """
    Pair-wise computation of sequences to generate hadamard (reciprocal) matrix
    Read from master data input file in chunks and process parallely on cluster HPC.

    :param(str) input_data_file_path: Master input data file, where each record is a single compute unit, i.e.,
        Comparison between two sequences to generate a hadamard matrix
    :param(int) chunk_size: No. of computation units per SLURM task
    :param(str) output_data_dir: Path to store output file of each SLURM task
    """
    slurm_task_id = int(os.environ.get('SLURM_ARRAY_TASK_ID'))
    print("Begin reciprocal process task ID: {}".format(slurm_task_id))
    grantham_subs_matrix_obj = utils.get_grantham_subs_matrix()
    with open(file=input_data_file_path, mode='r') as json_file:
        file_data = json.load(json_file)
    all_input_params = file_data['input_params']
    k = file_data['k']
    input_param_start_idx = slurm_task_id * chunk_size
    if input_param_start_idx > len(all_input_params):
        print('Start index {} exceeds total no of inputs: {}'.format(input_param_start_idx, len(all_input_params)))
        return
    output = []
    for input_entry in all_input_params[input_param_start_idx: input_param_start_idx + chunk_size]:
        try:
            hadamard_matrix = get_hadamard_matrix(
                sequence1=input_entry['sequence1'],
                sequence2=input_entry['sequence2'],
                k=k,
                substitution_matrix=grantham_subs_matrix_obj)
        except Exception as e:
            print("Error while generating reciprocal:\n{}\nSkipping..."
                  "\nSeq ID 1: {}; Seq ID 2: {}; K={}"
                  .format(str(e), input_entry['seq_id1'], input_entry['seq_id2'], k))
            continue

        data_to_save = {
            'seq_id1': input_entry['seq_id1'],
            'seq_id2': input_entry['seq_id2'],
            'sequence1': input_entry['sequence1'],
            'sequence2': input_entry['sequence2'],
            'k': k,
            'substitution_matrix': 'grantham',
            'hadamard_product': hadamard_matrix,
            'created_at': str(datetime.datetime.now())
        }
        output.append(data_to_save)
    print("Generated reciprocals for {} sequence pairs".format(len(output)))
    out_file_path = "{}/output_{}.json".format(output_data_dir, slurm_task_id)
    with open(file=out_file_path, mode='w') as json_file:
        json.dump(output, json_file)
    print("Output stored at {}".format(out_file_path))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate reciprocals for sequence pairs')
    parser.add_argument('input_data_file_path', help='Absolute path to master input data file (json)', type=str)
    parser.add_argument('--chunk_size', help='Chunk size for no. of computations in each parallel unit', type=int,
                        default=20)
    parser.add_argument('output_data_dir', help='Absolute path to directory where each process output will be stored',
                        type=str)
    args = parser.parse_args()
    start_time = time.time()
    process(input_data_file_path=args.input_data_file_path, chunk_size=int(args.chunk_size),
            output_data_dir=args.output_data_dir)
    print("Process was completed in {} secs".format(time.time() - start_time))
