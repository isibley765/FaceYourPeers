print("Importing python libraries, hang on...")

import os                   # This is a python library to work with files & folders
import cv2                  # This is OpenCV, a famous Computer Vision jack-of-all-trades library with a lot of fast, helpful tools
                                # Like image & video processing! You'll see this use that a bit
import numpy as np          # This is a library for matrixes and arrays -- that's fast at handling large, complicated ones
                                # Images can be loaded in as a large 2D or 3D matrix, hence why we'll use this -- cv2 will even use it by default 
import face_recognition     # Our main star -- a facial recognition library, already calibrated and ready to role! Just needs to be fed images

default_face_folder_location = "my_saved_faces/"
faces_templates = {}

if not os.path.isdir(default_face_folder_location):     # This folder holds the 
    os.makedirs(default_face_folder_location)

# Go through each person's folder (andassume it's named after the person) and save the name & their "face-print"
for name in os.listdir(default_face_folder_location):
    # save the folder we're currently working in; who's name folder we're scanning images from
    name_folderpath = os.path.join(default_face_folder_location, name)

    # make sure this path is to a folder, not a file
    if os.path.isdir(name_folderpath):
        print("Downloading {}'s face profile...\n".format(name))
        

        # if a previous file template has been saved, assume no images have been changed 
        if os.path.exists(os.path.join(name_folderpath, name + ".npz")):
            print("Saved face template exists! Loading it in now...")

            # add person's saved face template to our saved templates object
            faces_templates[name] = list(np.load(os.path.join(name_folderpath, name + ".npz"))["face_template"])

        # if no file template has been saved, upload all 
        else:
            print("Looking at {}'s face images:\n  {}".format(name, name_folderpath))
            current_face_templates = []
        
            for image in os.listdir(name_folderpath):     # Process each image of the person in their folder
                # save the image file's path that we're currently scanning
                names_current_imagepath = os.path.join(name_folderpath, image)
                
                # make sure path is to a file this time
                if os.path.isfile(names_current_imagepath):
                    print("      {} loading...".format(image))
                    # Load the image
                    current_image = face_recognition.load_image_file(names_current_imagepath)
                    # Load the image's face template -- assume the person's face is the only one in the photo! Or, the first seen
                    current_image_face_template = face_recognition.face_encodings(current_image)[0]

                    # Add template to our template list for this person
                    current_face_templates.append(current_image_face_template)
            
            faces_templates[name] = current_face_templates
            np.savez_compressed(os.path.join(name_folderpath, name), face_template=np.asarray(faces_templates[name]))
        
        print("{}'s face profile is complete!".format(name))


print("All faces processed!")

for face in os.listdir(default_face_folder_location):
    test_image = os.path.join(default_face_folder_location, face)
    matching_rating = {}

    if os.path.isfile(test_image):
        # Load the image
        current_image = face_recognition.load_image_file(test_image)
        # Load the image's face template -- assume the person's face is the only one in the photo! Or, the first seen
        current_image_face_template = face_recognition.face_encodings(current_image)[0]

        print("{} matches the following:".format(test_image))
        for name in faces_templates.keys():
            rating = face_recognition.face_distance(faces_templates[name], current_image_face_template)
            matching = face_recognition.compare_faces(faces_templates[name], current_image_face_template)

            print(rating)
            print(matching)