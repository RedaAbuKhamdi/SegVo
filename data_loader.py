import config
import numpy as np

from os import listdir
from os.path import isfile, join

def load_images()->np.ndarray:
    files = ["{0}/{1}".format(config.DATA_DIRECTORY, file) 
             for file in listdir(config.DATA_DIRECTORY) 
             if isfile(join(config.DATA_DIRECTORY, file))]
    for file in files:
        yield np.load(file)