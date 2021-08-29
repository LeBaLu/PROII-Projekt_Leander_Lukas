#      Python: 3.7.6
#   Kodierung: utf-8
#        Name: Leander Lukas
# Matrikelnr.: 802559
""" """
import logging


logging.basicConfig(filename='out.log', filemode='w', level=logging.INFO)


class SentParseGen():
    """ """
    def __init__(self, path):
        self.file = open(path, encoding='utf-8')
        self.gen = self.sent_parse_pair_generator()

    def sent_parse_pair_generator(self):
        current_line = next(self.file)
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
                    continue
                except StopIteration:
                    self.file.close()
                    return
            # Wordindex.
            i = 0
            while (current_line.strip()
            and current_line[0] != '#'):
                cells = current_line.split()[3:]
                cell_mat.append(cells)
                t = ''.join((t, cells[2].replace('*',
                f"({ cells[1] } { cells[0] }/{ i })")))
                try:
                    current_line = next(self.file)
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
