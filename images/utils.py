import cv2
import numpy as np
import pickle

def extract_features(image_path):
    img = cv2.imread(image_path, 0)
    orb = cv2.ORB_create()
    keypoints, descriptors = orb.detectAndCompute(img, None)
    return pickle.dumps(descriptors)  # Convert to binary for storage
