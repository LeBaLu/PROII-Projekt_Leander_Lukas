#      Python: 3.7.6
#   Kodierung: utf-8
#        Name: Leander Lukas
# Matrikelnr.: 802559
"""Selbstbenannte Fehlerklassen.

Hier sind die Ausnahmen, die bei fehlerhaftem oder unvollständigem Input
geworfen werden sollen, definiert.

"""
class SieveNotImplementedError(Exception):
    """Unknown-sieve-exception.

    Should be raised when unknown sieve-IDs are passed by the user.

    Arg:
        msg(str): Human readable string describing the exception.

    """
    def __init__(self, msg):
        super().__init__(msg)


def main():
    sieves = {'EMS', 'PCS'}
    def foo(s):
        if s in sieves:
            return 'success!'
        else:
            raise SieveNotImplementedError(f'{s} is not an existing sieve.')
    print(foo('PS'))


if __name__ == "__main__":
    main()
