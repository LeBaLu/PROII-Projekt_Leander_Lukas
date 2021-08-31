#      Python: 3.7.6
#   Kodierung: utf-8
#        Name: Leander Lukas
# Matrikelnr.: 802559
""" """
from sieve import AbstractSieve as abs
from sent_parse_iter import SentParseGen
from nltk.tree import Tree
import logging


logging.basicConfig(filename='out.log', filemode='w', level=logging.INFO)


class SieveFramework():
    """ """
    def __init__(self, path):
        self.generator = SentParseGen(path)

    def claim_mentions(self):
        """Creates the initial one-mention-clusters.

        Agreement information is encoded as follows:
            0 - singular, inanimate.
            1 - plural, 1st person, animate.
            2 - 2nd person.
            3 - 3rd person.

        Returns a tuple of:
            mentions(list of tuple(pair of list and nltk.Tree)): Each tuple
                                                                 contains the
                                                                 mentions
                                                                 (tuple) of a
                                                                 sentence in
                                                                 linear order
                                                                 (list) and
                                                                 the
                                                                 sentence's
                                                                 parse tree
                                                                 (nltk.Tree).
            clusters(dict): Cluster-IDs as keys and tuples of 4 sets as values
                            with the 1st set containing mentions as triples
                            of sentence-ID, the first word's ID and the last
                            word's ID, the 2nd set containing number
                            information, the 3rd containing person information
                            and the 4th containing animacy information.
            mentions_to_clusters(dict): Mentions(see clusters) as keys and
                                        cluster-IDs(int) as values.

        """
        # List of tuples containing a sentence's mentions and parse tree.
        mentions = []
        # Dictionary with Cluster-IDs(int) as keys and  tuples of sets
        # containing mentions and agreement information as values.
        clusters = dict()
        mentions_to_clusters = dict()
        sent_id = 0
        cluster_id = 0
        bftt = abs.breadth_first_tree_traversal
        # Generate sentence-parse pairs in the file.
        while True:
            try:
                sent, parse = next(self.generator)
            except StopIteration:
                break
            # Mentions in the current sentence.
            sent_mentions = []
            # Nltk.tree from the parse string of the current sentence.
            tree = Tree.fromstring(parse)
            # Save all NPs as mentions.
            for subtree in bftt(tree):
                # Template for cluster as it will be saved in the dictionary.
                atom_cluster = set(), set(), set(), set()
                # Index of 1st word of RE.
                start = int(subtree.leaves()[0].split('/')[-1])
                # Index of last word of RE.
                end = int(subtree.leaves()[-1].split('/')[-1])
                sent_mentions.append((start, end))
                long_mention = sent_id, start, end
                atom_cluster[0].add(long_mention)
                # True, once a number feature has been assigned to cluster.
                number = False
                # True, once a person feature has been assigned to cluster.
                person = False
                # Look for agreement information.
                for line in sent[start:end+1]:
                    # Plural?.
                    if (line[1] in ['NNS', 'NNPS']
                    or line[0].casefold() in ['we', 'they']):
                        atom_cluster[1].add(1)
                        number = True
                    # Singular?.
                    elif (line[1] in ['NN', 'NNP']
                    or line[0].casefold() in ['I', 'he', 'she', 'it']):
                        atom_cluster[1].add(0)
                        number = True
                    # 1st person?.
                    if line[0].casefold() in ['I', 'we']:
                        atom_cluster[2].add(1)
                        person = True
                    # 2nd person?.
                    elif line[0].casefold() in ['you']:
                        atom_cluster[2].add(2)
                        person = True
                    # 3rd person.
                    else:
                        atom_cluster[2].add(3)
                        person = True
                    if number and person:
                        break
                # Named entity information.
                nei = ''
                if (sent[start][7][0] == '('
                and sent[end][7][-1] == ')'):
                    for line in sent[start:end+1]:
                        nei = ''.join((nei, line[7]))
                    nei = nei.replace('*', '')
                if (nei
                and nei.count('(') == 1
                and nei.count(')') == 1):
                    if nei.strip(')(') == 'PERSON':
                        atom_cluster[3].add(1)
                    else:
                        atom_cluster[3].add(0)
                clusters[cluster_id] = atom_cluster
                mentions_to_clusters[long_mention] = cluster_id
                cluster_id += 1
            mentions.append((sent_mentions, tree))
            sent_id += 1
        return mentions, clusters, mentions_to_clusters


def main():
    obj1 = SieveFramework("flat_train_2012/bc_cctv_0001.v4_auto_conll")
    logging.info(obj1.claim_mentions()[1])


if __name__ == "__main__":
    main()
