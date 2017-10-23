# -*- coding: utf-8 -*-

import yaml

class ConfigAttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__


def load_config_file(filename="config.yml"):
    with open(filename, 'r') as ymlfile:
        return normalizer_config(yaml.load(ymlfile))



def normalizer_config(cfg):
    if isinstance(cfg,ConfigAttributeDict):
        return cfg

    # Absolute path to the directory in which the models should be created
    working_dir = cfg['working_dir']
    cfg['truecase_dataset'] = working_dir + cfg['truecase_dataset']

    # Training datasets
    cfg['train_orig'] = working_dir + cfg['train_orig']
    cfg['train_norm'] = working_dir + cfg['train_norm']

    # Location of the datasets for language modeling, the target-side training data is always used (does not have to be defined)
    # Experiments show that using multiple relevant target-language datasets as language models is the easiest way to improve your results
    cfg['lms'] = [cfg['train_orig'][:-4]]  # remove endings

    return ConfigAttributeDict(cfg)