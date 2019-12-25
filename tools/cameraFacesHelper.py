#!/usr/bin/env python3
#!/usr/bin/python3

import tools.mapfaceEncodings as mapf
import tools.helper_utils as util

import face_recognition as fr
import numpy as np
import json
import cv2
import os

def getPaddedBoundaries(face_location):
    top, right, bottom, left = face_location
    vert_pad = (bottom - top) // 7
    horiz_pad = (right - left) // 7

    top -= vert_pad
    bottom += vert_pad
    left -= horiz_pad
    right += horiz_pad

    return top, bottom, left, right

def outlineFaceInImage(faceimage, person):
    index, boundaries = util.largestFaceIndex(faceimage)
    top, bottom, left, right = getPaddedBoundaries(boundaries)
    
    cv2.rectangle(faceimage, (left, top), (right, bottom), (0, 0, 255), 2)
    cv2.rectangle(faceimage, (left, top-20), (right, top), (0, 0, 255), -1)
    cv2.putText(faceimage, person, (left, top), cv2.FONT_HERSHEY_SIMPLEX, .75, (255,255,255), 2)


    cv2.imshow(person, faceimage[:, :, ::-1]) # color adjustment for OpenCV, it's backwards
    cv2.waitKey(0)
    cv2.destroyAllWindows()