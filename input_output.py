#      Python: 3.7.6
#   Kodierung: utf-8
#        Name: Leander Lukas
# Matrikelnr.: 802559
""" """
from custom_exceptions import *
from framework import SieveFramework
import sys
import os


class PromptReader():
    """Handles input from the command line."""
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


def main():
    obj1 = PromptReader(['bla', 'refs/', 'exact_match', 'banana'])


if __name__ == "__main__":
    main()
