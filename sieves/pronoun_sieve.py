#      Python: 3.7.6
#   Kodierung: utf-8
#        Name: Leander Lukas
# Matrikelnr.: 802559
""" """
from sieve import AbstractSieve
import logging


logging.basicConfig(filename='out.log', filemode='w', level=logging.INFO)


class PronounSieve(AbstractSieve):
    """Sieve inspired by Ragunathan et al..

    For an explanation of the attributes see sieve.AbstractSieve.

    """
    def apply_sieve(self):
        """ """
        smbb = self.sort_mentions_by_bftt
        m_to_c = self.mentions_to_clusters
        # To keep track of the sentence number.
        sent_id = 0
        # Previous (mention_list, parse tree) pair.
        prev_pair = tuple()
        for mention_list, tree in self.mentions:
            # We work with (sentence, start, end) triples instead of
            # (start, end) pairs.
            comp = [(sent_id, start, end) for start, end in mention_list]
            universal_mentions = comp
            # Which mentions will be resolved by the sieve?.
            selected = self.select_mentions(universal_mentions,
                                            ignore_indef=True)
            # We aren't processing the first sentence currently.
            if prev_pair:
                prev_mentions, prev_tree = prev_pair
                prev_sent_antecedents = smbb(prev_mentions,
                                             prev_tree, sent_id-1)
            else:
                prev_sent_antecedents = []
            # Current mention index.
            i = 0
            for mention in universal_mentions:
                # CLuster the current mention belongs to.
                cluster = m_to_c[mention]
                info = self.clusters[cluster]
                tag_info = info[4]
                # Only resolve pronoun clusters.
                if (selected[i]
                and 1 in tag_info
                and len(tag_info) == 1):
                    same_sent_antecedents = universal_mentions[:i]
                    same_sent_antecedents.extend(prev_sent_antecedents)
                    antecedents = same_sent_antecedents
                    for antec in antecedents:
                        antec_cluster = m_to_c[antec]
                        # Are the mention and its antecedent already in the
                        # same cluster?.
                        if cluster != antec_cluster:
                            antec_info = self.clusters[antec_cluster]
                            feat_id = 1
                            skip = False
                            for feat in info[1:]:
                                antec_feat = antec_info[feat_id]
                                if not feat.intersection(antec_feat):
                                    # Ignore cases where animacy info wasn't
                                    # provided.
                                    if (feat_id == 3
                                    and (not feat or not antec_feat)):
                                        continue
                                    # Ignore definiteness violations.
                                    if feat_id == 5:
                                        continue
                                    skip = True
                                feat_id += 1
                            if not skip:
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
