import matplotlib.pyplot as plt
import pandas as pd
import collections as clt
import pickle as pkl
import numpy as np
import seaborn as sns
from pathlib import Path
from typing import List, Mapping

TYPE_SCORE_MATRIX = Mapping[str, Mapping[str, float]]

"""import local functions"""
from bio_shark import settings
from bio_shark.dive.prediction import Prediction

"""
THESE FUNCTIONS ARE MAINLY FOR VISUALIZING PREDICTION RESULTS AND SHOULD BE IMPORTED INTO THE NOTEBOOK.
"""

# PLOTTING PARAMETERS
fontsize='20'
title_fontsize='18'
markersize= '6'
plt.rcParams['font.sans-serif'] = "Arial"
plt.rcParams['font.family'] = "sans-serif"
plt.rcParams['axes.titlesize'] = title_fontsize
plt.rcParams['xtick.labelsize'] = fontsize
plt.rcParams['ytick.labelsize'] = fontsize
plt.rcParams['font.size'] = fontsize
plt.rcParams['figure.figsize'] = (6,6)
plt.rcParams['savefig.format'] = "svg"
plt.rcParams['legend.fontsize'] = int(fontsize)-9
plt.rcParams['lines.markersize'] = markersize
plt.rcParams['lines.marker'] = "o"
plt.rcParams['lines.linestyle'] = '--'
plt.rcParams['axes.linewidth'] = 2
plt.rcParams['legend.frameon']=False
cmap='gray_r'
seq1_color='darkgrey'
seq2_color='b'
fig_dpi=400

# plot dotplot of matched k-mers between 2 sequences
def plot_dotplot(testdf : pd.DataFrame, dname: str, ename: str, outfile: Path, ttype: str):
    """
    Visualize the similarity matrix between 2 sequence as a dotplot.
    Shade intensity indicates similarity of the k-mers between the two sequences.

    :param testdf: dataframe object of the similarity matrix between two sequences
    :param dname: name of query sequence
    :param ename: name of target sequence
    :param outfile: Path to output file
    :param ttype: score-type: SHARK-score (best), SHARK-score (T), or Normalised Google Distance
    :return df_to_nparray: Similarity matrix as a numpy array.
    Rows represent query k-mers and columns represent target k-mers.
    """
    df_to_nparray=testdf.to_numpy()
    sns.heatmap(df_to_nparray,vmin=0,vmax=1,linecolor=None,linewidths=0.2,cmap=cmap,cbar=False)
    plt.ylim(0,df_to_nparray.shape[0])
    plt.xlim(0,df_to_nparray.shape[1])
    plt.axhline(y=0, color='k',linewidth=2,ls='-',marker='')
    plt.axhline(y=df_to_nparray.shape[0], color='k',linewidth=2,ls='-',marker='')
    plt.axvline(x=0, color='k',linewidth=2,ls='-',marker='')
    plt.axvline(x=df_to_nparray.shape[1], color='k',linewidth=2,ls='-',marker='')
    length=len(list(testdf.columns)[0])
    plt.title(str(length)+'-mer Similarity Matrix, '+ttype)
    plt.xticks([])
    plt.yticks([])
    plt.xlabel(str(ename))
    plt.ylabel(str(dname))
    plt.tight_layout()
    plt.savefig(outfile, dpi=fig_dpi)
    plt.close()
    return df_to_nparray

# calculate amino acid composition of sequence (just a reference plot)
def aacomp(sequence: str):
    """
    Generate a dictionary of the amino acid frequency of the given sequence.

    :param sequence: amino acid sequence
    :return: dict[str, float] Key -> amino acid; Value -> frequency (amino acid frequency dictionary)
    """
    freq=clt.Counter(list(sequence))
    freq=clt.defaultdict(float,{k:v/len(sequence) for k,v in freq.items()})
    return freq

# plot amino acid composition of both sequences
def plot_aacomp(d: clt.defaultdict ,e: clt.defaultdict ,dname: str ,ename: str ,outfile: Path):
    """
    Visualize the amino acid frequencies of the sequences as a bar chart for comparison

    :param d: amino acid frequency dictionary
    :param e: amino acid frequency dictionary
    :param dname: name of query sequence
    :param ename: name of target sequence
    :param outfile: path to output figure file
    :return None
    """
    plt.figure(figsize=(6,6))
    for index,elem in enumerate(list('ACDEFGHILKMNPQRSTVWY')):
        plt.bar(index+1-0.2,d[elem]*100,width=0.4,color=seq1_color)
        plt.bar(index+1+0.2,e[elem]*100,width=0.4,color=seq2_color)
    plt.bar(10,0,color=seq1_color,label=dname)
    plt.bar(10,0,color=seq2_color,label=ename)
    plt.xticks(range(1,21,1),list('ACDEFGHILKMNPQRSTVWY'))
    plt.ylabel('% Frequency')
    plt.xlabel('Amino Acid')
    plt.legend(framealpha=0,loc='upper center')
    ax=plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig(outfile,dpi=fig_dpi)
    plt.close()
    return None

def create_boxplots(scorelist: List[float], outfile: Path, inpickle= settings.VISUALISATION_PKL_PATH):
    """
    Compare the k-mer scores between the sequences (i.e. input features into SHARK-dive), visualized as a horizontal line,
    to the distribution of unrelated (left, grey) and homologous (right, red) sequences.

    :param scorelist: list of scores
    :param outfile: Path to output figure file
    :param inpickle: Path to pickle file containing the distributions of input feature scores of homologous versus
    unrelated sequences (optional, default path is given)
    """
    with open(inpickle,'rb') as f:
        bplists=pkl.load(f)
    fig=plt.figure(figsize=(30,12))
    for index,(name,statsn,statss) in enumerate(bplists):
        ax=fig.add_subplot(2,5,index+1)
        ax.bxp(statsn, showfliers=False, showmeans=True,positions=[0.5],patch_artist = True,boxprops=dict(edgecolor='k',facecolor='k',alpha=0.3),whiskerprops=dict(marker=''),medianprops=dict(marker=''),capprops=dict(marker=''))
        ax.bxp(statss, showfliers=False, showmeans=True,positions=[1],patch_artist = True,boxprops=dict(edgecolor='r',facecolor='r',alpha=0.3),whiskerprops=dict(marker=''),medianprops=dict(marker=''),capprops=dict(marker=''))
        ax.axhline(scorelist[index],color='b',marker='')
        ax.set_xticklabels([])
        ax.set_xticks([])
        ax.set_title(name,fontsize=int(fontsize)+6)
    plt.tight_layout()
    plt.savefig(outfile,dpi=400)
    plt.show()
    plt.close()
    return None

def map_to_sequence(sim_matrix: TYPE_SCORE_MATRIX ,qseq: str, eseq: str,qname: str, ename: str, outfile: Path,ttype: str, k: int):
    """
    Visualize the k-mer matches between two sequences, defined by the similarity matrix (of a given score type)
    between them, in a dot plot. Dots represent regions along the sequences (starting from the bottom left)
    where there is a match.

    :param sim_matrix: similarity matrix object between 2 sequences.
    See core.SeqPairSimilarity generate_similarity_matrix function
    :param qseq: query sequence
    :param eseq: target sequence
    :param qname: query name
    :param ename: target name
    :param outfile: Path to output figure file
    :param ttype: score-type: SHARK-score (best), SHARK-score (T), or Normalised Google Distance
    :param k: k-mer length
    """
    qseq_kmers = [qseq[i:i + k] for i in range(len(qseq) - k + 1)]
    eseq_kmers=[eseq[i:i+k] for i in range(len(eseq) - k + 1)]
    df_to_nparray=np.zeros((len(qseq_kmers),len(eseq_kmers)))
    for (qkmeri,ekmeri), x in np.ndenumerate(df_to_nparray):
        df_to_nparray[qkmeri,ekmeri]=sim_matrix[qseq_kmers[qkmeri]][eseq_kmers[ekmeri]]
    sns.heatmap(df_to_nparray, vmin=0, vmax=1, linecolor=None, linewidths=0.2, cmap=cmap, cbar=False)
    plt.ylim(0, df_to_nparray.shape[0])
    plt.xlim(0, df_to_nparray.shape[1])
    plt.axhline(y=0, color='k', linewidth=2, ls='-', marker='')
    plt.axhline(y=df_to_nparray.shape[0], color='k', linewidth=2, ls='-', marker='')
    plt.axvline(x=0, color='k', linewidth=2, ls='-', marker='')
    plt.axvline(x=df_to_nparray.shape[1], color='k', linewidth=2, ls='-', marker='')
    plt.title(str(k) + '-mer Matches\n' + ttype)
    plt.xticks([])
    plt.yticks([])
    plt.xlabel(str(ename))
    plt.ylabel(str(qname))
    plt.tight_layout()
    plt.savefig(outfile, dpi=fig_dpi)
    plt.close()
    return None


if __name__ == '__main__':
    print("Running...")
    seq1_name = 'FUS_PLD'
    sequence1 = 'MASNDYTQQATQSYGAYPTQPGQGYSQQSSQPYGQQSYSGYSQSTDTSGYGQSSYSSYGQSQNTGYGTQSTPQGYGSTGGYGSSQSSQSSYGQQSSYPGYGQQPAPSSTSGSYGSSSQSSSYGQPQSGSYSQQPSYGGQQQSYGQQQSYNPPQGYGQQNQYNSSSGGGGGGGGGGNYGQDQSSMSSGGGSGGGYGNQDQSGGGGSGGYGQQ'
    seq2_name = 'CREST'
    sequence2 = 'NQNMQSLLPAPPTQNMNLGPGALTQSGSSQGLHSQGSLSDAISTGLPPSSLLQGQIGNGPSHVSMQQTAPNTLPTTSMSISGPGYSHAGPASQGVPMQGQGTIGNYVSRTNINMQSNPVSMMQQQAATSHYSSAQGGSQHYQGQSSIAMMGQGSQGSSMMGQRPMAPYRPSQQGSSQQYLGQEEYYGEQYSHSQGAAEPMGQQYYPDGHGDYAYQQSSYTEQSYDRSFEESTQHYYEGGNSQYSQQQAGYQQGAAQQQTYSQQQYPSQQSYPGQQQGYGSAQGAPSQYPGYQQGQGQQYGSYRAPQTAPSAQQQRPYGYEQGQYGNYQQ'

    # create sequencedicts:
    seq1dict = {seq1_name: sequence1}
    seq2dict = {seq2_name: sequence2}
    pred = Prediction(q_sequence_id_map=seq1dict, t_sequence_id_map=seq2dict).predict()
    pred_invert = [elem if i not in range(1, 4) else 1 - elem for i, elem in enumerate(pred[0]['similarity_scores_k'])]
    create_boxplots(pred_invert, '/Users/maxim/PycharmProjects/shark/similarity_matrices_newest/kmerscores_boxplot')
