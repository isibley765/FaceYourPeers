#!/usr/bin/env python3
#!/usr/bin/python3

import tools.helper_utils as util

import face_recognition as fr
import numpy as np
import json
import cv2
import os

# Assumes subfolders with names of subjects
def preloadedOrFreshEncodings(folderName="known_faces"):
    res = {}
    new_encodings = False

    # If the folder doesn't exist yet, make it
    if not os.path.isdir(folderName):
        os.makedirs(folderName)
        print("Given folder {}/ didn't exist -- creating it for you to fill".format(folderName))

    for person in os.listdir(folderName):
        curpath = os.path.join(folderName, person)
        if os.path.isdir(curpath):
            print("Loading {}'s face-recognition template...".format(person))
            res[person] = []    # Encodings for each person will be saved in a list

            # Check for self generated .npz files
            npz_present = False
            persons_files = os.listdir(curpath)
            for filename in persons_files:
                if filename.endswith(".npz"):
                    npz_present = True

            if npz_present:
                res[person] = list(readFaceEncodings(curpath, person))
            else:
                res[person].extend(getFaceEncodings(curpath, persons_files))
                writeOneFaceEncoding(res, curpath, person)

        else:
            print("{} isn't a directory...".format(person))
    
    return res

# Assumes subfolders with names of subjects
def getFaceEncodings(curpath, faces_list):
    # Ignore the self generated .npz filess
    names = []
    for image in faces_list:
        if not image.endswith(".npz"):
            imagepath = os.path.join(curpath, image)
            try:
                names.append(fr.load_image_file(imagepath))
            except:
                print("Failed to load -- are you sure this is an image?\n    {}".format(imagepath))

    return util.turnAllImagesToFeats(names)

# Assumes a directory with each sub directory being the name of the candidate
def readFaceEncodings(facepath, person):
    encodefile = os.path.join(facepath, "encodings_"+person+".npz")
    encoding = None

    if os.path.isfile(encodefile):
        npzclass = np.load(encodefile)

        for fn in npzclass.files:
            encoding = npzclass[fn]
    else:
        print("No encoded file detected at {}".format(facepath))
    
    return encoding

def writeAllFaceEncodings(encoded, outName="known_faces"):
    for person in encoded:
        encodefolder = os.path.join(outName, person)
        writeOneFaceEncoding(encoded, encodefolder, person)

def writeOneFaceEncoding(encoded, encodefolder, person):
    encodefile = os.path.join(encodefolder, "encodings_"+person)
    array = np.asarray(encoded[person])

    if not os.path.isdir(encodefolder):
        os.makedirs(encodefolder)
    print(encodefile)
    print(array.shape)
    np.savez_compressed(encodefile, array)

if __name__ == "__main__":
    res = preloadedOrFreshEncodings()
    writeAllFaceEncodings(res)
    # known = preloadedOrFreshEncodings()
    # print(known["Ian"])
    # print(util.compareListToKnown(known["Ian"], known))