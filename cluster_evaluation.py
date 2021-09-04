#      Python: 3.7.6
#   Kodierung: utf-8
#        Name: Leander Lukas
# Matrikelnr.: 802559
"""Berechnung des paarweisen F1-Scores."""
from sent_parse_iter import SentParseGen
from framework import SieveFramework
import logging


logging.basicConfig(filename='out.log', filemode='w', level=logging.INFO)


class ConllClusterEvaluator():
    """For comparing read and calculated clusters.

    Args:
        path(str): Directory of a conll-file we use to calculate
                   clusters with sieves and extract the given clusters.
        sieve_appliance(list of str): The sieves and the order they're applied
                                      in.

    """
    def __init__(self, path, sieve_appliance):
        self.path = path
        self.sieve_appliance = sieve_appliance

    @staticmethod
    def add_mention(d, key, val):
        """Adds a value to a set in a dictionary.

        Args:
            d(dict): Dictionary with sets as values.
            key: Identifier of a set within d.
            val: Element to be added to the set identified by key.

        Returns:
            d(dict): Dictionary with val in one of its sets.

        """
        if key in d:
            d[key].add(val)
        else:
            d[key] = {val}
        return d

    def extract_clusters(self):
        """Retrieves gold clusters from the file.

        Returns:
            clusters(dict): Holds cluster-IDs(int) as keys and sets of
                            (sent_id, start, end)-triples as values.

        """
        generator = SentParseGen(self.path)
        sent_id = 0
        clusters = dict()
        while True:
            try:
                sent, parse = next(generator)
            except StopIteration:
                break
            # Nesting level of a mention.
            level = 0
            # Keeps track of the nesting level a mention is on and its start
            # index.
            mention_info = dict()
            word_id = 0
            for word in sent:
                coref_infos = word[-1].split('|')
                for info in coref_infos:
                    if not len(info) == 1:
                        # Start of a mention?.
                        if info[0] == '(':
                            # Single word mention?.
                            if info[-1] == ')':
                                clust = int(info.strip(')('))
                                clusters = self.add_mention(clusters, clust,
                                                            (sent_id, word_id,
                                                             word_id))
                            else:
                                level += 1
                                mention_info[level] = (int(info.strip(')(')),
                                                       word_id)
                        # End of a mention.
                        else:
                            clust, start = mention_info[level]
                            clusters = self.add_mention(clusters, clust,
                                                        (sent_id, start,
                                                         word_id))
                            level -= 1
                word_id += 1
            sent_id += 1
        return clusters

    def calculate_clusters(self):
        """Employs the multi-pass sieve to link mentions.

        Returns:
            clusters(dict): Holds cluster-IDs(int) as keys and sets of
                            (sent_id, start, end)-triples as values.

        """
        clusters = dict()
        framework = SieveFramework(self.path, self.sieve_appliance)
        ments, clusts, ments_to_clusts, s_l_dict = framework.multi_pass_sieve()
        clusters = {k: v[0] for (k, v) in clusts.items()}
        return clusters

    @staticmethod
    def pair_mentions(clusters):
        """Creates pairings of mentions in the same cluster.

        Arg:
            clusters(dict): Holds cluster-IDs(int) as keys and sets of
                            (sent_id, start, end)-triples as values.

        Returns:
            pairs(set): Collection of all possible combinations(set) of two
                        mentions belonging to the same cluster.

        """
        pairs = set()
        for clust in clusters:
            mentions = clusters[clust]
            # It takes two to make a pair.
            if len(mentions) == 1:
                continue
            # Contains the mentions that have already been paired with every
            # other mention in the cluster.
            without = set()
            for ment1 in mentions:
                without.add(ment1)
                for ment2 in mentions.difference(without):
                    pairs.add(frozenset({ment1, ment2}))
        return pairs

    @classmethod
    def pair_wise_f1_score(cls, gold_clusters, siev_clusters):
        """Calculates the F1-score for the results of coreference resolution.

        Args:
            gold_clusters(dict): Cluster-IDs(int) as keys and sets of
                                 (sent_id, start, end)-triples as values.
                                 Represents actual positives (P).
            siev_clusters(dict): Cluster-IDs(int) as keys and sets of
                                 (sent_id, start, end)-triples as values.
                                 Represents predicted positives (PP).

        Returns:
            f1_score(float): Harmonic combination of precision and recall when
                             comparing sets of mention-pairings.

        """
        P = cls.pair_mentions(gold_clusters)
        PP = cls.pair_mentions(siev_clusters)
        TP = P.intersection(PP)
        cardinal_P = len(P)
        cardinal_PP = len(PP)
        cardinal_TP = len(TP)
        PPV = cardinal_TP / cardinal_PP
        TPR = cardinal_TP / cardinal_P
        f1_score = 2 * ((PPV * TPR) / (PPV + TPR))
        return f1_score

    def multi_pass_sieve_pair_f1(self):
        """Wraps the whole class into a single method to get the F1-score.

        Returns:
            f1_score(float): Harmonic combination of precision and recall for
                             the multi-pass sieve method for coreference
                             resolution.

        """
        gold_clusters = self.extract_clusters()
        siev_clusters = self.calculate_clusters()
        f1_score = self.pair_wise_f1_score(gold_clusters, siev_clusters)
        return f1_score


def main():
    direc = "flat_train_2012/bc_cctv_0002.v4_auto_conll"
    # Precise Constructs first, pronouns second:
    logging.info('F1 (EM, PC, P):')
    obj1 = ConllClusterEvaluator(direc, ['exact_match', 'precise_constructs',
                                         'pronouns'])
    obj1_f1 = obj1.multi_pass_sieve_pair_f1()
    logging.info(f"{obj1_f1:.4f}")
    # Pronouns first, precise constructs second:
    logging.info('F1 (EM, P, PC):')
    obj2 = ConllClusterEvaluator(direc, ['exact_match', 'pronouns',
                                         'precise_constructs'])
    obj2_f1 = obj2.multi_pass_sieve_pair_f1()
    logging.info(f"{obj2_f1:.4f}")


if __name__ == "__main__":
    main()
