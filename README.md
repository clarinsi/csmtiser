# cSMTiser
A tool for text normalisation via character-level machine translation

## Prerequisites

The tool requires the following tools to be installed:

* moses decoder + KenLM (http://www.statmt.org/moses/?n=Development.GetStarted)
* mgiza (https://github.com/moses-smt/mgiza). Installation instructions for mgiza can be found [here](http://www.statmt.org/moses/?n=Moses.ExternalTools#ntoc3). Compiling MGIZA requires the Boost library, which can be installed by running `sudo apt-get install libboost-all-dev` command

Additionally, the tool expects basic bash functionality and can therefore be run on *NIX systems / environments only.

## Running the tool

Running the tool consists of the following steps:
- configuring the normaliser
- training data preprocessing
- building the models and tuning the system
- running the final normaliser

We exemplify each step on a dataset of Slovene tweets. The initial data can be found in ```tweets_sl.orig``` and ```tweets_sl.norm```.

### Configuring your normaliser

The first step is to let the normaliser know where to find components of the Moses SMT system and to define various parameters.

To perform configuration, go through the ```config.py``` script and change values of variables where necessary. Comments inside the code should help you during the process.

### Data preprocessing

The first, optional step in preprocessing is tokenisation. The exemplary datasets are already tokenised (spaces before punctuation etc.), so this process is, as stated in the configuration file, not run.

To fight data sparseness (you never have enough manually normalised data to have seen all the phenomena) we either perform truecasing or lowercasing of the data.

Truecasing s a method that calculates the statistics for each word regarding the case (lowercase, uppercase) it was seen when not at the beginning of the sentence. The most frequent case is then enforced on all sentence beginnings.

Lowercasing is a more agressive way to fight data sparsness than truecasing. In case of using lowercasing, all text normalised will be lowercased as well. This method should be applied if (1) there is not much data (less than a few million tokens) to learn a decent truecaser or (2) casing is not used in a consistent or traditional (beginning of sentence) way, like in user-generated content. We perform truecasing on our exemplary dataset just to showcase the truecasing method, although lowercasing would be a more reasonable option in our case.

After truecasing or lowercasing, the dataset is split into train and dev data (if no extra development data is made available) and transformed to the format necessary for learning the models.

Our examplary run of this step produces the following output:

```
$ python preprocess.py
Learning the truecaser
Truecasing tweet_sl.orig
Truecasing tweet_sl.norm
Truecasing tweet_sl
Reading data for splitting into train and dev
Splitting the data
Preparing the data for learning models
```

The process produces the training (```train.orig``` and ```train.norm```) and development datasets (```dev.orig``` and ```dev.norm```), as well as one dataset per each additional language model, in our case ```lm_0.proc```.

### Building the models and tuning the system

Building specific models and tuning the overall system is performed with one script, ```train.py```.

The script takes, as the ```preprocess.py``` script, parameters from the ```config.py``` script.

The exemplary run of this step produces the following output (logging the output of the training and tuning tools to ```train.log```):

```
$ python train.py
Deleting old models in the working directory
Building a LM from /home/nikola/tools/clarinsi/csmtiser//train.norm
Building a LM from tweet_sl
Building the untuned system
Updating the moses.ini file
Tuning the system
```

During the first runs the logging script ```train.log``` should be analysed to make sure that all the processes were finished successfully. This wrapper does not do much in reporting errors, just logs the output of the wrapped tools.

Additionally, training the exemplary system on 23 server-grade cores takes 2.3 hours (all together 47 CPU hours), so running the training procedure in background is probably a good idea. The simplest way to do so on a *NIX is this:

```
$ nohup python train.py &
```

### Running the normaliser

The final normaliser is run through the ```normalise.py``` script, where the first argument is the file whose content has to be normalised. The output is stored to the same path extended with the extension ```.norm```.

Logging of the normalisation process is performed in ```norm.log``` in the working directory.

The exemplary normaliser can be run like this:

```
python normalise.py text_to_normalise.txt
```

The output is available in ```text_to_normalise.txt.norm```. If tokenisation or truecasing are performed during data preparation, the reverse processes are run at the end of the normalisation process.

On our exemplary dataset detruecasing is performed, while detokenisation is not.
