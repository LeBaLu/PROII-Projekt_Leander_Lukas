#      Python: 3.7.6
#   Kodierung: utf-8
#        Name: Leander Lukas
# Matrikelnr.: 802559
""" """
from sieve import AbstractSieve
import logging


logging.basicConfig(filename='out.log', filemode='w', level=logging.INFO)


class SieveFramework(AbstractSieve):
    """ """
    def __init__(path, mentions, clusters, mention_to_cluster):
        super().init(mentions, clusters, mention_to_cluster)
        self.generator = SentParseGen(path)


def main():
    pass


if __name__ == "__main__":
    main()