#      Python: 3.7.6
#   Kodierung: utf-8
#        Name: Leander Lukas
# Matrikelnr.: 802559
""" """
from sieve import AbstractSieve
import logging


logging.basicConfig(filename='out.log', filemode='w', level=logging.INFO)


class ExactMatchSieve(AbstractSieve):
    """Sieve inspired by Ragunathan et al.."""
    def apply_sieve(self):
        """Matches mentions eith the same extent.

        Ignores personal pronouns.

        """
        smbb = self.sort_mentions_by_bftt
        wsft = self.word_string_from_tree
        m_to_c = self.mentions_to_clusters
        # To keep track of the sentence number.
        sent_id = 0
        # Previous (mention_list, parse tree) pair.
        prev_pair = tuple()
        for mention_list, tree in self.mentions:
            # We work with (sentence, start, end) triples instead of
            # (start, end) pairs.
            universal_mentions = [(sent_id, start, end) for start, end in mention_list]
            # Which mentions will be resolved by the sieve?.
            selected = self.select_mentions(universal_mentions)
            # Current mention index.
            i = 0
            for mention in universal_mentions:
                if selected[i]:
                    # CLuster the current mention belongs to.
                    cluster = m_to_c[mention]
                    # Mention words.
                    words = wsft(tree, mention[1], mention[2])
                    same_sent_antecedents = universal_mentions[:i]
                    # We aren't processing the first sentence currently.
                    if prev_pair:
                        prev_mentions, prev_tree = prev_pair
                        if 1 in self.clusters[cluster][4]:
                            continue
                        else:
                            prev_sent_ants = smbb(prev_mentions, prev_tree,
                                                  sent_id-1, l_to_r=False)
                    else:
                        prev_sent_ants = []
                    for antec in same_sent_antecedents:
                        antec_cluster = m_to_c[antec]
                        # Are the mention and its antecedent already in the
                        # same cluster?.
                        if cluster != antec_cluster:
                            ant_words = wsft(tree, antec[1], antec[2])
                            # Do the strings match exactly?.
                            if words == ant_words:
                                self.merge_clusters(cluster, antec_cluster)
                                cluster = m_to_c[mention]
                    for antec in prev_sent_ants:
                        antec_cluster = m_to_c[antec]
                        # Are the mention and its antecedent already in the
                        # same cluster?.
                        if cluster != antec_cluster:
                            ant_words = wsft(prev_tree, antec[1], antec[2])
                            # Do the strings match exactly?.
                            if words == ant_words:
                                self.merge_clusters(cluster, antec_cluster)
                                cluster = m_to_c[mention]
                i += 1
            sent_id += 1
            prev_pair = universal_mentions, tree


def main():
    # Siehe framework.py für Demonstrationen.
    pass


if __name__ == "__main__":
    main()
