import data_reader as reader
import data_loader as loader
import cv2

reader.prepare_data()
for img in loader.load_images():
    cv2.imshow("test", img)
    cv2.waitKey(0)