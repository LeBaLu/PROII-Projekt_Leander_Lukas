#      Python: 3.7.6
#   Kodierung: utf-8
#        Name: Leander Lukas
# Matrikelnr.: 802559
"""Funktionalitäten zum Einlesen einer conll-Datei."""
import logging


logging.basicConfig(filename='out.log', filemode='w', level=logging.INFO)


class SentParseGen():
    """Line-list-parse-tree-generator for conll-files.

    Arg:
        path(str): Directory of the conll-file.

    """
    def __init__(self, path):
        #: _io.TextIOWrapper: The file's line generator.
        self.file = open(path, encoding='utf-8')
        # The generator used by __next__().
        self.gen = self.sent_parse_pair_generator()
        #: dict: The ids of sentences as keys and their starting lines as
        #        values.
        self.sent_line_dict = dict()

    def sent_parse_pair_generator(self):
        """Generator of tuples.

        Yields:
            cell_mat(list of list of str): Nested list containing the lines of
                                           a sentence in the conll-format.
            t(str): The sentence's parse tree as a string that can easily be
                    converted by nltk.tree.

        """
        current_line = next(self.file)
        # Keeps track of sentence number.
        sent_id = -1
        # Keeps track of line.
        line_id = 1
        # Sentence (nested list of str).
        cell_mat = []
        # Treestring.
        t = ''
        while True:
            # Ignore the lines for which this holds true.
            if (not current_line.strip()
            or current_line[0] == '#'):
                try:
                    current_line = next(self.file)
                    line_id += 1
                    continue
                except StopIteration:
                    self.file.close()
                    return

            # Wordindex.
            i = 0
            sent_id += 1
            self.sent_line_dict[sent_id] = line_id
            while (current_line.strip()
                   and current_line[0] != '#'):
                cells = current_line.split()[3:]
                cell_mat.append(cells)
                new_child = f"({ cells[1] } { cells[0] }/{ i })"
                t = ''.join((t, cells[2].replace('*', new_child)))
                try:
                    current_line = next(self.file)
                    line_id += 1
                except StopIteration:
                    self.file.close()
                    return cell_mat, t.replace('(', ' (')[1:]
                i += 1
            yield cell_mat, t.replace('(', ' (')[1:]
            cell_mat = []
            t = ''

    def __next__(self):
        return next(self.gen)


def main():
    # How to generate all lines from the first file of the Ontonotes training
    # data.
    obj1 = SentParseGen("flat_train_2012/bc_cctv_0001.v4_auto_conll")
    while True:
        try:
            sent, parse = next(obj1)
        except StopIteration:
            break
        logging.info((sent, parse))


if __name__ == "__main__":
    main()
