#      Python: 3.7.6
#   Kodierung: utf-8
#        Name: Leander Lukas
# Matrikelnr.: 802559
"""Abstrakte Siebklasse."""
from abc import ABC, abstractmethod
from nltk.tree import Tree
import logging


class AbstractSieve(ABC):
    """ """
    def __init__(self, mentions, clusters):
        self.mentions = mentions
        self.clusters = clusters


def main():
    pass


if __name__ == "__main__":
    main()
