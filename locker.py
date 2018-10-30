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

# Get user supplied values
imagePath = "./motion_images/autolock_motion.jpg"
gap_sample_max = 1
sleep_time_lock = 1


def detect_person(person_name):
    # Read the image
    image = cv2.imread(imagePath)
    image = imutils.resize(image, width=450)

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Load encoded faces
    logger.debug("loading encodings...")
    data = pickle.loads(open(person_name + "_encodings.pickle", "rb").read())

    # Detect the (x, y)-coordinates of the bounding boxes corresponding to each face in the input frame, then compute
    # the facial embeddings for each face
    boxes = face_recognition.face_locations(rgb, model="cnn")
    encodings = face_recognition.face_encodings(rgb, boxes)

    matches = [False]

    # Loop over the facial embeddings
    for encoding in encodings:
        # attempt to match each face in the input image to our known encodings
        matches = face_recognition.compare_faces(data["encodings"], encoding)

    if True in matches:
        logger.debug(person_name.capitalize() + " is detected... :)")
        return True
    else:
        logger.debug("There is no " + person_name.capitalize())
    return False


# note: python version is 2.7!
def turn_on_motion():
    os.system('pkill -f motion')
    sleep(3)
    os.system('motion -c motion.conf start')
    sleep(4)


def main():
    turn_on_motion()
    last_time = 0
    gap_sample_cnt = 0
    person_name = ''

    imagePaths = paths.list_images("my_photos")
    for (i, path) in enumerate(imagePaths):
        person_name = path.split(os.path.sep)[-2]

    while True:
        # count = 0
        # while (count < 15):
        pic_time = os.path.getmtime(imagePath)
        logger.debug("pic_time is: %s" % pic_time)
        logger.debug("now      is: %s" % time.time())

        if pic_time == last_time and (pic_time + 15) >= time.time():
            gap_sample_cnt += 1
            if gap_sample_cnt >= gap_sample_max:
                is_face = detect_person(person_name)
                if not is_face:
                    gap_sample_cnt = 0
                    logger.debug("No faces, locking screen...")
                    os.system('setxkbmap -option grp:alt_shift_toggle us,ru')  # switch keyboard to US
                    os.popen('gnome-screensaver-command --lock')
                else:
                    logger.debug("detected face")
        else:
            logger.debug("there is an ongoing motion OR nothing happened for last 15 seconds. doing nothing...")

        sleep(sleep_time_lock)
        last_time = pic_time
        # count += 1


if __name__ == '__main__':
    main()
