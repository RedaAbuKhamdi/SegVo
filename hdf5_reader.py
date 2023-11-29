import config
import numpy as np
import h5py

def read_image(path : str)->np.ndarray:
    file = h5py.File(path, 'r')
    dset = file['data']['value']
    for i in range(dset.shape[0]-1):
        data = np.array(dset[i,:,:,:])
        print(data.shape)
        data = np.moveaxis(data, [0, 1, 2], [2, 1, 0])
        yield data