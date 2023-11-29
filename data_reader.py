import json
import numpy as np
import config

from os import listdir
from os.path import isfile, join
import image_reader
import hdf5_reader

_required_keys = ["directories", "formats"]
_available_formats = ['png', 'hdf5', 'h5']
_strategies = {
    image_reader : ['png'],
    hdf5_reader: ['hdf5', 'h5']
}
def _get_settings()->dict[str, str]:
    """Read JSON settings from settings.json in project root directory.

       Required keys in settings.json: ["directories", "formats"]
       directories is a list of strings describing paths to folders with images
       formats is a list of strings describing formats of images
       Available formats are: ['png']
       Raises:
       FileNotFoundError if settings.json is not found in project root directory
       JSONDecodeError if invalid JSON syntax
       ValueError if unexpected values detected in required json keys
    """
    settings = {}
    with open("settings.json", "r") as file:
        settings = json.loads(file.read())
        if set(_required_keys) != set(settings.keys()):
            raise KeyError("Required keys missing!")
        elif set(settings['formats']).union(set(_available_formats)) != set(_available_formats):
            raise ValueError("Unexpected formats values")
    return settings

def _read_directory(directory : str, formats : list[str])->np.ndarray:
    files = ["{0}/{1}".format(directory,file) 
             for file in listdir(directory) 
             if isfile(join(directory, file)) and file.split(".")[-1] in formats]
    for file in files:
        for strategy, strategy_formats in _strategies.items():
            if file.split(".")[-1] in strategy_formats:
                for img in strategy.read_image(file):
                    yield img
                break

def _save_data(data : np.ndarray, index : int):
    np.save("{0}/{1}.npy".format(config.DATA_OUTPUT_DIRECTORY, index), data, allow_pickle=False)
    return index + 1

def prepare_data():
    settings = _get_settings()
    i = 0
    for directory in settings['directories']:
        for image in _read_directory(directory, settings['formats']):
            i = _save_data(image, i)
    
