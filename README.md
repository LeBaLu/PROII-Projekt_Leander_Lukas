### NAME
A Multi-Pass Sieve for Coreference Resolution - Find english equivalents for german connectors in sentence-aligned texts.

### TABLE OF CONTENTS
1. [ Description ](#description)
2. [ Requirements ](#requirements)
3. [ Usage ](#usage) 
4. [ Author ](#author)


### DESCRIPTION
This program is a shred of an implementation of the multi-pass sieve propagated by Ragunathan et al., 2010 for coreference resolution. Referring expressions are transformed into clusters of agreement features, which then are sequentially merged through the appliance of different rules or *sieves*.


### REQUIREMENTS
The program is tested with python 3.7.6.


#### Corpus
I used the flat_train_2012-folder from the [ontonotes corpus](https://github.com/ontonotes/conll-formatted-ontonotes-5.0/releases/tag/v12), but any folder containing solely files in the conll-format should be fine.


#### Install NLTK
With anaconda or `pip`:
```
conda install -c anaconda nltk
pip install --user -U nltk
```

### USAGE

Our results are provided in the directory `results/`. To make the programm perform multi-pass sieve coreference resolution on your data follow these instructions:

First, place the data you want to process in the project directory, be that a single file or a folder containing a whole corpus.

Then you run the following command in the working directory on a console. Placeholders are uppercase.
```
python resolve DIRECTORY_TO_YOUR_DATA
```

#### Sieves
Additionally you can specify the sieves to use and in which order by adding their respective IDs to the command:

**exact_match** - for the exact-match sieve

**precise_constructs** - for the precise-constructs sieve

**pronouns** - for the pronoun sieve

For example: a call for applying the exact-match sieve and the pronoun sieve looks like this:
```
python DIRECTORY_TO_YOUR_DATA exact_match pronouns
```

The results.csv can be found in `os.getcwd()/results/`.


### AUTHOR
Leander Lukas
