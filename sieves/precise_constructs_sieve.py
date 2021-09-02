#      Python: 3.7.6
#   Kodierung: utf-8
#        Name: Leander Lukas
# Matrikelnr.: 802559
""" """
from sieve import AbstractSieve
import logging


logging.basicConfig(filename='out.log', filemode='w', level=logging.INFO)


class PreciseConstructsSieve(AbstractSieve):
    """Sieve inspired by Ragunathan et al.."""
    def apply_sieve(self):
        """ """
        smbb = self.sort_mentions_by_bftt
        wsft = self.word_string_from_tree
        # To keep track of the sentence number.
        sent_id = 0
        # Previous (mention_list, parse tree) pair.
        prev_pair = tuple()
        for mention_list, tree in self.mentions:
            # We work with (sentence, start, end) triples instead of
            # (start, end) pairs.
            universal_mentions = [(sent_id, start, end) for start, end in mention_list]
            # Which mentions will be resolved by the sieve?.
            selected = self.select_mentions(universal_mentions, ignore_indef=True)
            # Current mention index.
            i = 0
            for mention in universal_mentions:
                if selected[i]:
                    # CLuster the current mention belongs to.
                    cluster = self.mentions_to_clusters[mention]
                    mention_start = mention[1]
                    # Mention words.
                    words = wsft(tree, mention_start, mention[2])
                    same_sent_antecedents = universal_mentions[:i]
                    # We aren't processing the first sentence currently.
                    if prev_pair:
                        prev_mentions, prev_tree = prev_pair
                        if 1 in self.clusters[cluster][4]:
                            prev_sent_antecedents = smbb(prev_mentions,
                                                         prev_tree, sent_id-1)
                        else:
                            prev_sent_antecedents = smbb(prev_mentions,
                                                         prev_tree, sent_id-1,
                                                         l_to_r=False)
                    else:
                        prev_sent_antecedents = []
                    for antec in same_sent_antecedents:
                        antec_cluster = self.mentions_to_clusters[antec]
                        # Are the mention and its antecedent already in the
                        # same cluster?.
                        if cluster != antec_cluster:
                            antec_end = antec[2]
                            # Do the mention and its antecedent have a single word
                            # between them?.
                            if mention_start - antec_end == 2:
                                gap_id = mention_start - 1
                                gap_word = wsft(tree, gap_id, gap_id)
                                # Apposition or copulative relation?.
                                if gap_word in [',', ':', '-', 'is', 'are',
                                                "'re", 'am', "'m", 'was',
                                                'were']:
                                    self.merge_clusters(cluster, antec_cluster)
                                    cluster = self.mentions_to_clusters[mention]
                                    continue
                            ant_words = wsft(tree, antec[1], antec_end)
                            # Acronym?.
                            if words.isupper():
                                antec_acro = ''
                                for token in ant_words.split():
                                    antec_acro = "".join((antec_acro, token.upper()))
                                if antec_acro == words:
                                    self.merge_clusters(cluster, antec_cluster)
                                    cluster = self.mentions_to_clusters[mention]
                                    continue
                            elif ant_words.isupper():
                                ment_acro = ''
                                for token in words.split():
                                    ment_acro = "".join((ment_acro, token.upper()))
                                if ment_acro == ant_words:
                                    self.merge_clusters(cluster, antec_cluster)
                                    cluster = self.mentions_to_clusters[mention]
                    for antec in prev_sent_antecedents:
                        antec_cluster = self.mentions_to_clusters[antec]
                        # Are the mention and its antecedent already in the
                        # same cluster?.
                        if cluster != antec_cluster:
                            ant_words = wsft(prev_tree, antec[1], antec[2])
                            # Acronym?.
                            if words.isupper():
                                antec_acro = ''
                                for token in ant_words.split():
                                    antec_acro = "".join((antec_acro, token.upper()))
                                if antec_acro == words:
                                    self.merge_clusters(cluster, antec_cluster)
                                    cluster = self.mentions_to_clusters[mention]
                                    continue
                            elif ant_words.isupper():
                                ment_acro = ''
                                for token in words.split():
                                    ment_acro = "".join((ment_acro, token.upper()))
                                if ment_acro == ant_words:
                                    self.merge_clusters(cluster, antec_cluster)
                                    cluster = self.mentions_to_clusters[mention]
                i += 1
            sent_id += 1
            prev_pair = universal_mentions, tree


def main():
    # Siehe framework.py für Demonstrationen.
    pass


if __name__ == "__main__":
    main()
