#!/usr/bin/env python3
#!/usr/bin/python3

import face_recognition as fr
import numpy as np
import json
import cv2
import os

# Use the area of the bounding box as the "largest face" finder
def largestFaceIndex(faceimage):
    face_locations = fr.face_locations(faceimage)
    area = []

    for top, right, bottom, left in face_locations:
        area.append( (bottom - top) * (right - left) )
    
    index = area.index(max(area))
    
    return (index, face_locations[index])

# Turns images into the 128 feature list/vector
def turnAllImagesToFeats(images):
    res = []

    for image in images:
        largest_feats = TurnImageToFeats(image)

        if not largest_feats is None:
            res.append(largest_feats)
        
    return res

def TurnImageToFeats(image):
    res = None

    # Find face encodings
    face_encodings = fr.face_encodings(image)
    index = 0

    # Find the one with the most area (i.e. "biggest")
    if len(face_encodings) > 1:
        index, _ = largestFaceIndex(image)
            
    # Append the biggest/only face encoding, if available
    if len(face_encodings) > 0:
        res = face_encodings[index]
    
    return res

# Compares a list of features against a list of known vectors
def compareListToKnown(inlist, known_loaded=None, encode_path="known_faces"):
    if known_loaded is None:
        known_loaded = preloadedOrFreshEncodings(folderName=encode_path)
    
    res = {}

    for person in known_loaded:
        temp = []
        for el in inlist:
            temp.extend(fr.compare_faces(known_loaded[person], el))

        if len(temp):
            res[person] = temp.count(True) / len(temp)
        else:
            res[person] = 0

    return res

# Compares a list of features against a list of known vectors
def compareToKnown(image, known_loaded=None, encode_path="known_faces"):
    if known_loaded is None:
        known_loaded = preloadedOrFreshEncodings(folderName=encode_path)
    
    res = {}

    for person in known_loaded:
        res[person] = fr.compare_faces(known_loaded[person], image)

    return res