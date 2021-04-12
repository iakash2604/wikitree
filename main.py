import argparse
from wikitree import *

parser = argparse.ArgumentParser()
parser.add_argument('--create_graph', default=False, type=bool,
                    help='displays image of generated graph')
parser.add_argument('--single_branch', default=None,
                    help='Enter word or link to get its origin')
parser.add_argument('--wordbag_path', default=None,
                    help='Make graph of bunch of words')
args = parser.parse_args()


single_branch = args.single_branch
wordbag_path = args.wordbag_path
create_graph = args.create_graph

if single_branch is not None:
    edge_set = make_single_branch(single_branch)
    if create_graph:
        draw_graph(edge_set)

if wordbag_path is not None:
    wordbag = import_words(wordbag_path)
    edge_set = make_growing_branch(wordbag)
    if create_graph:
        draw_graph(edge_set)
