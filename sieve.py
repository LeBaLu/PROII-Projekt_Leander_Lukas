#      Python: 3.7.6
#   Kodierung: utf-8
#        Name: Leander Lukas
# Matrikelnr.: 802559
"""Abstrakte Siebklasse."""
from nltk.tree import Tree
from sent_parse_iter import SentParseGen
import logging


logging.basicConfig(filename='out.log', filemode='w', level=logging.INFO)


class AbstractSieve():
    """ """
    def __init__(self, path, mentions=[],
                 clusters=[], mention_to_cluster=dict()
                                        ):
        self.generator = SentParseGen(path)
        self.mentions = mentions
        self.clusters = clusters
        self.mention_to_cluster = mention_to_cluster

    @staticmethod
    def breadth_first_tree_traversal(tree, label_in=['NP', 'NX'], left_to_right=True):
        """ """
        # Next node to be expanded.
        act_node = tree
        frontier = [tree]
        trees_out = []
        if left_to_right:
            step_size = 1
        else:
            step_size = -1
        while frontier:
            act_node = frontier[0]
            if type(act_node) is Tree:
                if act_node.label() in label_in:
                    trees_out.append(act_node)
                for child in act_node[::step_size]:
                    logging.info(frontier)
                    frontier.append(child)
            frontier.pop(0)
        return trees_out


def main():
    obj1 = AbstractSieve("flat_train_2012/bc_cctv_0001.v4_auto_conll")
    tree = Tree('S', [Tree('NP', ['the', 'cat']), Tree('VP', ['ate'])])
    # Right to left breadth first traversal of NPs in tree.
    NPs1 = AbstractSieve.breadth_first_tree_traversal(tree, left_to_right=False)
    logging.info(NPs1)


if __name__ == "__main__":
    main()
