import numpy as np
import cv2

def read_image(path : str)->np.ndarray:
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    yield img