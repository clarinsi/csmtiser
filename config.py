# -*- coding: utf-8 -*-

import yaml
import os

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
    cfg['truecase_dataset'] = os.path.join(working_dir, cfg['truecase_dataset'])

    # Training datasets
    cfg['train_orig'] = os.path.join(working_dir, cfg['train_orig'])
    cfg['train_norm'] = os.path.join(working_dir, cfg['train_norm'])

    return ConfigAttributeDict(cfg)
