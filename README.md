# cSMTiser
A tool for text normalisation via character-level machine translation

Running the presumes an existing installation of the Moses SMT system. The final section of this README deals with installing Moses.

Running the tool consists of the following steps:
- configuring the normaliser
- data preprocessing
- training the models
- tuning the system
- running the final normaliser

We exemplify each step on a dataset of Slovene tweets. The initial data can be found in ```tweets_sl.orig``` and ```tweets_sl.norm```.

## Configuring your normaliser

The first step is to let the normaliser know where to find components of the Moses SMT system and to define various parameters.

For performing configuration, go through the ```config.py``` script and change values of variables where necessary. Code comments should help you in that process.

## Data preprocessing

The first, optional step in preprocessing is tokenisation. The exemplary datasets are already tokenised (spaces before punctuation etc.), so this process is, as stated in the configuration file, is not run.

To fight data sparseness (you never have enough manually normalised data to have seen all the phenomena), we first perform truecasing. This is a method that calculates the statistics for each word in what case (lowercase, other) it was seen when not at the beginning of the sentence. The most frequent case is then enforced on all sentence beginnings.

A more agressive way to fight data sparsness is to simply lowercase the whole dataset. In that case all the normalised text will be lowercased as well. This method should be applied if (1) there is not much data (less than a few million tokens) to learn a decent truecaser or (2) casing is not used in the traditional way, like in user-generated content. We perform truecasing on our dataset just to showcase the method while lowecasing would be a more reasonable option in our case.

After truecasing or lowercasing, the dataset is split into train and dev data (if so defined) and transformed to the format necessary for learning models.

An example run of this step follows:

```
$ python preprocess.py
Learning the truecaser
Truecasing tweet_sl.orig
Truecasing tweet_sl.norm
Truecasing tweet_sl
Reading data for splitting into train and dev
Splitting the data
Preprocessing the data for learning models
```

Exemplary outputs of the process can be observed in ```tweet_sl.orig.train.proc``` or ```lm_0.proc``` (the data for the first additional language model).

