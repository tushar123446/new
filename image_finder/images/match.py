import cv2
import os
import numpy as np
from django.conf import settings
from images.models import StoredImage

def find_best_match(object_image_path):
    object_img = cv2.imread(object_image_path)
    if object_img is None:
        return None
    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(cv2.cvtColor(object_img, cv2.COLOR_BGR2GRAY), None)
    if des1 is None:
        return None
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    best_match = None
    max_score = 0
    threshold = 10  # ✅ Minimum number of good matches to consider it a real match

    for stored in StoredImage.objects.all():
        img_path = os.path.join(settings.MEDIA_ROOT, stored.image.name)
        img = cv2.imread(img_path)
        if img is None:
            continue

        kp2, des2 = orb.detectAndCompute(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), None)
        if des2 is None:
            continue

        matches = bf.match(des1, des2)
        score = len(matches)

        print(f"🔍 Matching with {stored.image.name}: Score = {score}")

        if score > max_score and score > threshold:  # ✅ Only if score crosses threshold
            max_score = score
            best_match = stored

    return best_match



def detect_object(image_path):
    detected_objects = ["car", "bottle", "phone"]  # Simulated list
    print("Detected objects:", detected_objects)  
    return detected_objects

