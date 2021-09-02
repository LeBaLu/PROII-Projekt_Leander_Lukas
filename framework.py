#      Python: 3.7.6
#   Kodierung: utf-8
#        Name: Leander Lukas
# Matrikelnr.: 802559
""" """
from sieve import AbstractSieve as abs
from sent_parse_iter import SentParseGen
from sieves import *
from nltk.tree import Tree
import logging


logging.basicConfig(filename='out.log', filemode='w', level=logging.INFO)


class SieveFramework():
    """ """

    id_to_sieve = {'exact_match': exact_match_sieve.ExactMatchSieve,
                   'precise_constructs':
                   precise_constructs_sieve.PreciseConstructsSieve,
                   'pronouns': pronoun_sieve.PronounSieve}

    def __init__(self, path, sieve_appliance=['exact_match',
                                              'precise_constructs',
                                              'pronouns']):
        self.generator = SentParseGen(path,
                                      sent_to_line=('saves/',
                                      ''.join((path.split('/')[-1][:-14],
                                      '_sentence_to_line.csv'))))
        self.sieve_appliance = sieve_appliance

    def claim_mentions(self):
        """Creates the initial one-mention-clusters.

        Agreement information is encoded as follows:
            0 - singular, inanimate, tagged as sth else or longer than one
                word, indefinite.
            1 - plural, 1st person, animate, tagged as PRP, definite.
            2 - 2nd person, tagged as NNP.
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
            clusters(dict): Cluster-IDs as keys and tuples of 6 sets as values
                            with the 1st set containing mentions as triples
                            of sentence-ID, the first word's ID and the last
                            word's ID, the 2nd set containing number
                            information, the 3rd containing person
                            information, the 4th containing animacy
                            information, the 5th containing tag information
                            and the 6th containing definiteness information.
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
                atom_cluster = set(), set(), set(), set(), set(), set()
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
                # PRP or NNP?.
                if start == end:
                    if sent[start][1] == 'PRP':
                        atom_cluster[4].add(1)
                    elif sent[start][1] == 'NNP':
                        atom_cluster[4].add(2)
                    else:
                        atom_cluster[4].add(0)
                else:
                    atom_cluster[4].add(0)
                # Definiteness.
                if sent[start][0].casefold() in ['a', 'an', 'some', 'other',
                                                 'one', 'someone', 'anyone',
                                                 'everyone', 'anybody',
                                                 'everybody', 'nobody',
                                                 'somebody', 'another',
                                                 'either', 'neither', 'each',
                                                 'little', 'less', 'much',
                                                 'both', 'few', 'fewer',
                                                 'many', 'others', 'several',
                                                 'all', 'any', 'more', 'most',
                                                 'none']:
                    atom_cluster[5].add(0)
                else:
                    atom_cluster[5].add(1)
                clusters[cluster_id] = atom_cluster
                mentions_to_clusters[long_mention] = cluster_id
                cluster_id += 1
            mentions.append((sent_mentions, tree))
            sent_id += 1
        return mentions, clusters, mentions_to_clusters

    def multi_pass_sieve(self):
        """ """
        ments, clusts, ments_to_clusts = self.claim_mentions()
        for sieve_id in self.sieve_appliance:
            sieve = self.id_to_sieve[sieve_id](ments, clusts, ments_to_clusts)
            sieve.apply_sieve()
            ments = sieve.mentions
            clusts = sieve.clusters
            ments_to_clusts = sieve.mentions_to_clusters
        return ments, clusts, ments_to_clusts


def main():
    obj1 = SieveFramework("flat_train_2012/bc_cctv_0001.v4_auto_conll")
    #m1, c1, m_to_c1 = obj1.claim_mentions()
    #logging.info(c1)
    m2, c2, m_to_c2 = obj1.multi_pass_sieve()
    logging.info(c2)


if __name__ == "__main__":
    main()
