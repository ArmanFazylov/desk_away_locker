#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import sys
import os
import time
import pickle
import imutils
import face_recognition
from imutils import paths
import logging
from logging.handlers import RotatingFileHandler
from time import sleep

# configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='/tmp/desk_away_app.log',
                    filemode='w')
logger = logging.getLogger('my_logger')
handler = RotatingFileHandler('/tmp/desk_away_app.log', maxBytes=2000, backupCount=10)
logger.addHandler(handler)
## stout logging
logger.addHandler(logging.StreamHandler())


def capture_photos(name):
    path = 'my_photos/' + name
    if not os.path.exists(path):
        os.makedirs(path)

    for i in range(10):
        logger.info('Press Enter to capture a photo ' + str(i + 1))
        cap = cv2.VideoCapture(0)  # video capture source camera (Here webcam of laptop)
        ret, frame = cap.read()  # return a single frame in variable `frame`
        cv2.imshow(name + '_' + str(i + 1), frame)  # display the captured image

        if cv2.waitKey(0) & 0xFF == ord('\r'):  # save on pressing 'Enter'
            cv2.imwrite(os.path.join(path, 'image_' + str(i + 1) + '.jpg'), frame)
            cv2.destroyAllWindows()
            cap.release()
            continue

def encode_faces(firstname):
    imagePaths = list(paths.list_images('my_photos')) # grab the paths to the input images in our dataset
    knownEncodings = []
    knownNames = ['Arman']
    for (i, imagePath) in enumerate(imagePaths): # loop over the image paths
        logger.info('Processing image {}/{}'.format(i + 1, len(imagePaths))) # extract the person name from the image path
        name = imagePath.split(os.path.sep)[-2]
        # load the input image and convert it from RGB (OpenCV ordering) to dlib ordering (RGB)
        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # detect the (x, y)-coordinates of the bounding boxes corresponding to each face in the input image
        boxes = face_recognition.face_locations(rgb, model='cnn')
        # compute the facial embedding for the face
        encodings = face_recognition.face_encodings(rgb, boxes)
        # loop over the encodings
        for encoding in encodings:
            # add each encoding + name to our set of known names and encodings
            knownEncodings.append(encoding)
            knownNames.append(name)
        # dump the facial encodings + names to disk
        logger.info('Serializing encodings...')
        data = {'encodings': knownEncodings, 'names': knownNames}
        f = open(firstname + '_encodings.pickle', 'wb')
        f.write(pickle.dumps(data))
        f.close()
        # do a bit of cleanup
        cv2.destroyAllWindows()

def main():
    # turn off motion and locker.py
    os.system('pkill -f motion')
    sleep(3)
    os.system('pkill -f locker.py')

    name = input('Please enter your first name: ')
    name = name.lower()
    logger.info('You entered ' + str(name))
    capture_photos(name)
    sleep(1)
    logger.info('Photos are captured. Starting training...')
    sleep(1)
    encode_faces(name)

if __name__ == '__main__':
    main()
