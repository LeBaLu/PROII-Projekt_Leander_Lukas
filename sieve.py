#      Python: 3.7.6
#   Kodierung: utf-8
#        Name: Leander Lukas
# Matrikelnr.: 802559
"""Abstrakte Siebklasse."""
from abc import ABC, abstractmethod
from nltk.tree import Tree
import logging


logging.basicConfig(filename='out.log', filemode='w', level=logging.INFO)


class AbstractSieve(ABC):
    """Template of a sieve-class and collection of useful methods.

    

    """
    def __init__(self, mentions, clusters, mentions_to_clusters):
        self.mentions = mentions
        self.clusters = clusters
        self.mentions_to_clusters = mentions_to_clusters

    @staticmethod
    def breadth_first_tree_traversal(tree, label_in=['NP', 'NX'], left_to_right=True):
        """Does breadth-first search for subtrees with certain labels.

        Args:
            tree(nltk.tree.Tree): The tree that is traversed.
            label_in(:obj:'list'of'str', optional): Subtrees with these labels
                                                    are returned. Defaults to
                                                    a list of NP-labels.
            left_to_right(:obj:'bool', optional): Levels of the tree are
                                                  traversed from left to
                                                  right, if True or from right
                                                  to left, if False. Defaults
                                                  to True.

        Returns:
            trees_out(list of nltk.tree.Tree): The desired subtrees in the
                                               order they have been visited
                                               in.

        """
        # Next node to be expanded.
        act_node = tree
        # Queue of nodes to be visited.
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
                    frontier.append(child)
            frontier.pop(0)
        return trees_out

    @staticmethod
    def word_string_from_tree(tree, start, end):
        """Gives the mention the shape of a string.

        Args:
            tree(nltk.Tree): The parse tree of a sentence.
            start(int): Index of the first word of the mention.
            end(int): Index of the last word of the mention.

        Returns:
            word_string(str): The words of the mention's phrase seperated by
                              whitespaces.

        """
        word_string = ""
        for leaf in tree.leaves()[start:end+1]:
            word_string = ' '.join((word_string,
                                    "/".join(leaf.split('/')[:-1])))
        return word_string.strip()

    @classmethod
    def sort_mentions_by_bftt(cls, mention_list, tree, sent_id, l_to_r=True):
        """Sorts a list of triples according to a tree.

        Args:
            mention_list(list of tuple): Mentions that are to be sorted.
            tree(nltk.Tree): The tree whose breadth-first traversal determines
                             the sorting order of the mentions.
            sent_id(int): Index of the sentence, the mentions belong to.
            l_to_r(:obj:'bool', optional): Determines whether the levels of
                                           the tree are traversed from left to
                                           right, if True or from right to
                                           left, if False.

        Returns:
            sorted_list(list of tuple): A list of triples sorted by
                                        breadth-first tree traversal according
                                        to the respective parse tree.

        """
        bftt = cls.breadth_first_tree_traversal
        sorted_list = []
        for subtree in bftt(tree, left_to_right=l_to_r):
            start = int(subtree.leaves()[0].split('/')[-1])
            end = int(subtree.leaves()[-1].split('/')[-1])
            sorted_list.append((sent_id, start, end))
        return sorted_list

    def select_mentions(self, mention_list, ignore_indef=False):
        """Decides which mentions to resolve with a sieve.

        Arg:
            mention_list(list of tuple): Mentions, whose resolving we make a
                                         decision about.
            ignore_indef(:obj:'bool', optional): Mentions from clusters
                                                 containing indefinite
                                                 elements are categorically
                                                 not resolved, if True.
                                                 Defaults to False.

        Returns:
            to_select(list of bool): Records the result of each decision in
                                     the same order that the mentions appear
                                     in mention_list in.

        """
        # To keep track of clusters whose first occurence was already given
        # the permission to be resolved.
        existing_clusters = set()
        # Who are our candidates?.
        to_select = []
        pos = 0
        for mention in mention_list:
            cluster = self.mentions_to_clusters[mention]
            # Don't resolve the first mention in the list.
            if pos == 0:
                to_select.append(False)
                existing_clusters.add(cluster)
                pos += 1
                continue
            # Don't resolve clusters with indefinite feature.
            elif ignore_indef and 0 in self.clusters[cluster][5]:
                to_select.append(False)
                existing_clusters.add(cluster)
                continue
            # Only resolve the first appearance of a cluster.
            elif cluster in existing_clusters:
                to_select.append(False)
                pos += 1
                continue
            to_select.append(True)
            existing_clusters.add(cluster)
            pos += 1
        return to_select

    def merge_clusters(self, a, b):
        """Combines two clusters into one.

        The resulting cluster always retains the smaller cluster-ID and
        discards the bigger one.

        Args:
            a(int): Cluster-ID of the cluster to be merged with cluster b.
            b(int): Cluster-ID of the cluster to be merged with cluster a.

        """
        # ID of cluster that keeps its ID.
        orig = min((a, b))
        # ID of cluster that loses its ID.
        spec = max((a, b))
        # Assign new cluster-ID in reference dictionary.
        for mention in self.clusters[spec][0]:
            self.mentions_to_clusters[mention] = orig
        # Join mention and feature sets together.
        orig_sets = list(self.clusters[orig])
        for i in range(len(orig_sets)):
            s = orig_sets[i]
            orig_sets[i] = s.union(self.clusters[spec][i])
        self.clusters[orig] = tuple(orig_sets)
        del self.clusters[spec]

    @abstractmethod
    def apply_sieve(self):
        """Will merge clusters, if conditions are met.

        Has to be implemented in every subclass.

        """
        pass


def main():
    # Dieser Code funktioniert nur, wenn man den abstractmethod-Decorator
    # auskommentiert, da eine abstrakte Klasse selbst nicht instanziiert
    # werden sollte.
    obj1 = AbstractSieve([(0, 0, 0), (1, 0, 0), (2, 3, 5)],
                         {0: ({(0, 0, 0)}, {0}),
                          1: ({(1, 0, 0), (2, 3, 5)}, {1})
                                                          },
                         {(0, 0, 0): 0, (1, 0, 0): 1, (2, 3, 5): 1})
    logging.info(obj1.select_mentions(obj1.mentions))
    obj1.merge_clusters(0, 1)
    logging.info(obj1.clusters)
    logging.info(obj1.mentions_to_clusters)
    tree = Tree('S', [Tree('NP', ['the', 'cat']), Tree('VP', ['ate'])])
    # Right to left breadth first traversal of NPs in tree.
    NPs1 = AbstractSieve.breadth_first_tree_traversal(tree,
                                                      left_to_right=False)
    logging.info(NPs1)


if __name__ == "__main__":
    main()
