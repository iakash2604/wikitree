import argparse
from wikitree import *

parser = argparse.ArgumentParser()
parser.add_argument('--create_graph', default=False, type=bool,
                    help='displays image of generated graph')
parser.add_argument('--single_branch', default=None,
                    help='Enter word or link to get its wiki branch')
parser.add_argument('--wordbag_path', default=None,
                    help='Path to wordbag file. Generates a self growing wiki branch from wordbag')
parser.add_argument('--stop_at_philosophy', default=None,
                    help='Stop growth of branch if philosophy node has been reached')
args = parser.parse_args()


single_branch = args.single_branch
wordbag_path = args.wordbag_path
create_graph = args.create_graph
stop_at_philosophy = args.stop_at_philosophy

if single_branch is not None:
    edge_set = make_single_branch(
        single_branch, stop_at_philosophy,  "#1e90ff")
    if create_graph:
        draw_graph(edge_set)

if wordbag_path is not None:
    wordbag = import_words(wordbag_path)
    edge_set = colored_growing_branch(wordbag, stop_at_philosophy)
    if create_graph:
        draw_graph(edge_set)
