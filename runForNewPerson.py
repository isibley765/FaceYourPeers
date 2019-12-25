#!/usr/bin/env python3
#!/usr/bin/python3

import tools.cameraFacesHelper as faceCam
import tools.mapfaceEncodings as mapf
import tools.helper_utils as util

import face_recognition as fr
import numpy as np
import json
import cv2
import os

face_templates = "./known_faces/"
faces_to_identify = "./run_faces/"

encoded_people = mapf.preloadedOrFreshEncodings(folderName=face_templates)



if not os.path.isdir(faces_to_identify):
    os.makedirs(faces_to_identify)

for image in os.listdir(faces_to_identify):
    curpath = os.path.join(faces_to_identify, image)
    if os.path.isfile(curpath):
        image_array = fr.load_image_file(curpath)
        face_feature_vector = util.TurnImageToFeats(image_array)

        matches = util.compareToKnown(face_feature_vector, known_loaded=encoded_people)

        for person in matches:
            if matches[person].count(True) > matches[person].count(False):
                faceCam.outlineFaceInImage(image_array, person)

