# -*- coding: utf-8 -*-

import os
import sys

from csmtiser import Csmtiser
from csmtiser.config import load_config_file

if __name__ == "__main__":
  if len(sys.argv) > 2:
    normalizer = Csmtiser(load_config_file(sys.argv[1]))
    path=sys.argv[2]
  else:
    normalizer = Csmtiser(load_config_file())
    path=sys.argv[1]

  pth=normalizer.normalise(pth = path)
  os.system('mv ' + pth + ' ' + path + '.norm')
