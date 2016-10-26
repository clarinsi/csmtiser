# cSMTiser
A tool for text normalisation via character-level machine translation

## Prerequisites

The tool requires the following tools to be installed:

* moses decoder + KenLM (http://www.statmt.org/moses/?n=Development.GetStarted)
* mgiza (https://github.com/moses-smt/mgiza)

Additionally, the tool expects basic bash functionality and can therefore be run on *NIX systems / environments only.

## Running the tool

Running the tool consists of the following steps:
- configuring the normaliser
- data preprocessing
- building the models and tuning the system
- running the final normaliser

We exemplify each step on a dataset of Slovene tweets. The initial data can be found in ```tweets_sl.orig``` and ```tweets_sl.norm```.

### Configuring your normaliser

The first step is to let the normaliser know where to find components of the Moses SMT system and to define various parameters.

For performing configuration, go through the ```config.py``` script and change values of variables where necessary. Code comments should help you in that process.

### Data preprocessing

The first, optional step in preprocessing is tokenisation. The exemplary datasets are already tokenised (spaces before punctuation etc.), so this process is, as stated in the configuration file, is not run.

To fight data sparseness (you never have enough manually normalised data to have seen all the phenomena), we first perform truecasing. This is a method that calculates the statistics for each word in what case (lowercase, other) it was seen when not at the beginning of the sentence. The most frequent case is then enforced on all sentence beginnings.

A more agressive way to fight data sparsness is to simply lowercase the whole dataset. In that case all the normalised text will be lowercased as well. This method should be applied if (1) there is not much data (less than a few million tokens) to learn a decent truecaser or (2) casing is not used in the traditional way, like in user-generated content. We perform truecasing on our exemplary dataset just to showcase the truecasing method while lowercasing would be a more reasonable option in our case.

After truecasing or lowercasing, the dataset is split into train and dev data (if so defined) and transformed to the format necessary for learning models.

Our examplary run of this step produces the following output:

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

The process produces the training (```train.orig``` and ```train.norm```) and development datasets (```dev.orig``` and ```dev.norm```), as well as one dataset per language model, in our case , two Exemplary results of the process can be observed in ```train.orig``` or ```lm_0.proc``` (the data for the first additional language model).

### Building the models and tuning the system

Both building specific models and tuning the overall system is performed with one script, ```train.py```.

The script takes, as the ```preprocess.py``` script, parameters from the ```config.py``` script.

The exemplary run of this step produces the following output (logging the verbatim output of the tools to ```train.log```):

```
$ python train.py
Deleting old models in the working directory
Building a LM from /home/nikola/tools/clarinsi/csmtiser//train.norm
Building a LM from tweet_sl
Building the untuned system
Updating the moses.ini file
Tuning the system
```

During the first runs the logging script should be analysed in detail to make sure that all the processes were finished successfully. This wrapper does not handle reporting errors as the underlying system does not do that neither.

Additionally, training the exemplary system on 23 server-grade cores takes multiple hours, so running the training procedure in background is probably a good idea. The simplest way to do so on a *NIX is this:

```
$ nohup python train.py &
```

### Running the normaliser

The final normaliser is run through the ```normalise.py``` script, sending the original text to standard input and receiving it on standard output.

The exemplary normaliser can be run like this:

```
echo 'Nevem komboš to povedu' | python normalise.py
Ne vem kom boš to povedal
```