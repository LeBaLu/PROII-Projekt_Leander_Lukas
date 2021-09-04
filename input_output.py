#      Python: 3.7.6
#   Kodierung: utf-8
#        Name: Leander Lukas
# Matrikelnr.: 802559
""" """
from custom_exceptions import *
from framework import SieveFramework
import multiprocessing as mp
import csv
import os
import logging


logging.basicConfig(filename='out.log', filemode='w', level=logging.INFO)


class PromptReader():
    """Handles input from the command line.

    Arg:
        console_input(list): Command that is executed.

    """
    def __init__(self, console_input):
        direc = console_input[1]
        if os.path.exists(direc):
            self.direc = direc
        else:
            raise FileNotFoundError('The path you entered leads nowhere.')
        if len(console_input) > 2:
            sieve_appliance = console_input[2:]
            for sieve_id in sieve_appliance:
                if sieve_id not in SieveFramework.id_to_sieve:
                    raise SieveNotImplementedError(f'No sieve by the name of'\
                                                   f' {sieve_id} has been im'\
                                                   f'plemented to date.')
            self.sieve_appliance = sieve_appliance
        else:
            self.sieve_appliance = ['exact_match', 'precise_constructs',
                                    'pronouns']

    @staticmethod
    def data_files(path):
        """Lists the files in a directory.

        Arg:
            path(str): Directory of a file or a folder containing files.

        Returns:
            files(list): Name(s) of the file(s) under the directory.

        """
        files = []
        # The user wants to process files in a folder.
        if path[-1] == '/':
            folder_files = os.listdir(path)
            files = [''.join((path, name)) for name in folder_files]
        # The user wants to process a single file.
        else:
            files.append(path)
        return files

    @staticmethod
    def perform_mps(file, sieve_appliance):
        """Performs multi-pass-sieve coreference resolution on a file.

        Args:
            file(str): Directory of the file whose coreference properties
                       interest us.
            sieve_appliance(list of str): Sieves and the order in which they
                                          are to be applied.

        Returns:
            file_name(str): The filename without the extension.
            clusters(dict): Cluster-IDs(int) as keys and sets of
                            (start_line, end_line)-tuples as values.

        """
        framework = SieveFramework(file, sieve_appliance=sieve_appliance)
        ments, clusts, m_to_c, sent_to_line = framework.multi_pass_sieve()
        # Dispose of unneeded information.
        clusters = {k: v[0] for (k, v) in clusts.items()}
        # IDs of single word clusters we will remove.
        to_remove = []
        # Translate (sent_id, start, end)- into (start_line, end_line)-tuples.
        for key in clusters:
            if len(clusters[key]) == 1:
                to_remove.append(key)
                continue
            old_mentions = []
            new_mentions = []
            for sent_id, start_word, end_word in clusters[key]:
                sent_start = sent_to_line[sent_id]
                start_line = sent_start + start_word
                end_line = sent_start + end_word
                old_mentions.append((sent_id, start_word, end_word))
                new_mentions.append((start_line, end_line))
            # Remove mentions in the by-sentence format and add those in the
            # line-no format.
            for i in range(len(old_mentions)):
                clusters[key].remove(old_mentions[i])
                clusters[key].add(new_mentions[i])
        for key in to_remove:
            del clusters[key]
        file_name = file.split('.')[0].split('/')[-1]
        return file_name, clusters

    def write_results(self, path_to_results='results/result.csv'):
        """Writes clusters to a csv-file.

        Args:
            path_to_results(:obj:'str', optional): Precise directory/name of
                                                   the save file. Defaults to
                                                   'results/result.csv'

        """
        folder = '/'.join(path_to_results.split('/')[:-1])
        if not os.path.exists(folder):
            os.mkdir(folder)
        if os.path.exists(path_to_results):
            os.remove(path_to_results)
        files = self.data_files(self.direc)
        appliances = [self.sieve_appliance]*len(files)
        arguments = zip(files, appliances)
        with mp.Pool() as pool:
            file_clusters = pool.starmap(self.perform_mps, arguments)
        for f, cs in file_clusters:
            with open(path_to_results, 'a', newline='') as csv_out:
                outwriter = csv.writer(csv_out)
                outwriter.writerow([f])
                for c_id in cs:
                    mentions = []
                    for x, y in cs[c_id]:
                        # Don't save single word mentions as spans.
                        if x == y:
                            mentions.append(str(x))
                        else:
                            mentions.append(" - ".join((str(x), str(y))))
                    outwriter.writerow([c_id]+mentions)


def main():
    # Run resolve for real demonstration.
    # Throws error because of wrong sieve.
    obj1 = PromptReader(['bla', 'refs/', 'exact_match', 'banana'])


if __name__ == "__main__":
    main()
