from ..core.utils import read_fasta_file
from ..dive.run import run_normal, run_sparse
from ..core.alf_scoring import get_google_distance_score
import time
import resource
import argparse
from pathlib import Path
from .. import settings


def main():
    # START TIMING
    start = time.time()

    parser = argparse.ArgumentParser(
        description="Run SHARK-Scores (best or T=x variants) or Normalised Google Distance Scores. "
        "Note that if a FASTA file is provided, it will be used instead."
    )
    parser.add_argument(
        'query',
        help="Query sequence",
        type=str,
        nargs='?',
        default=None
    )
    parser.add_argument(
        'target',
        help="Target sequence",
        type=str,
        nargs='?',
        default=None
    )
    parser.add_argument(
        '--infile', '-i',
        help="Query FASTA file",
        type=str,
        default=None
    )
    parser.add_argument(
        '--dbfile', '-d',
        help="Target FASTA file",
        type=str,
        default=None
    )
    parser.add_argument(
        '--outfile', '-o',
        help="Result file",
        type=str,
    )
    parser.add_argument(
        '--scoretype', '-s',
        help="Score type: best or threshold or NGD. Default is threshold.",
        type=str,
        choices=['best', 'threshold', 'NGD'],
    )
    parser.add_argument(
        '--length', '-k',
        help="k-mer length",
        type=int,
    )
    parser.add_argument(
        '--threshold', '-t',
        help="threshold for SHARK-Score (T=x) variant",
        type=float,
    )

    # PARSE ARGUMENTS
    args = parser.parse_args()
    infile = args.infile
    dbfile = args.dbfile
    outfile_p = args.outfile
    scoretype = args.scoretype
    k = args.length
    threshold = args.threshold
    query_seq = args.query
    target_seq = args.target

    # READ IN FASTA FILES IF PROVIDED. IF NOT, READ IN SEQUENCES
    if infile:
        inseqs = read_fasta_file(Path(infile))
    else:
        if not any(aa not in settings.CANONICAL_AAS for aa in query_seq):
            inseqs = {query_seq: query_seq}
        else:
            raise Exception('Query sequence contains non-canonical AAs.')
    if dbfile:
        dbseqs = read_fasta_file(Path(dbfile))
    else:
        if not any(aa not in settings.CANONICAL_AAS for aa in target_seq):
            dbseqs = {target_seq: target_seq}
        else:
            raise Exception('Target sequence contains non-canonical AAs.')

    # SET SCORE SUBTYPE
    sparse_flag = False
    google_flag = False
    if scoretype == 'best':
        sparse_flag = True
    elif scoretype == 'NGD':
        google_flag = True

    c = 0
    n_set = 0

    # DEFINE OUTPUT file and LOG file (which logs memory usage and time)
    outfile = Path(outfile_p)
    logfile = Path(outfile.as_posix()+'.log')

    with open(outfile, 'w+') as f:
        f.write("Query\tTarget\tScore")
        for qid, qseq in inseqs.items():
            for eid, eseq in dbseqs.items():
                c += 1
                if c == 10000:
                    n_set += 1
                    print(f"Completed {n_set*10000} comparisons")
                    print(f"Memory Usage: {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}")
                    print(f"Time Elapsed: {time.time()-start}")
                    c = 0
                if sparse_flag:
                    f.write('\n' + qid + '\t' + eid + '\t' + str(run_sparse(qseq, eseq, k)))
                elif google_flag:
                    f.write('\n' + qid + '\t' + eid + '\t' + str(get_google_distance_score(qseq, eseq, k)))
                else:
                    f.write('\n' + qid + '\t' + eid + '\t' + str(run_normal(qseq, eseq, k, threshold)))

    with open(logfile, 'w+') as of:
        end = time.time()
        of.write(f"Time Taken: {end-start} SECONDS\n")
        of.write(f"Memory Usage: {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss} KB\n")
        of.write('Run Complete.')
        print(f"{k}-mer Scores Done! Results saved to {outfile.as_posix()}")


if __name__ == "__main__":
    main()
