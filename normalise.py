# -*- coding: utf-8 -*-

import os
import sys

from csmtiser import Csmtiser
from csmtiser.config import load_config_file

if __name__ == "__main__":
    normalizer = Csmtiser(load_config_file())
    pth=normalizer.normalise(pth = sys.argv[1])


    os.system('mv ' + pth + ' ' + sys.argv[1] + '.norm')

