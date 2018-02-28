#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import sys
import os
import time
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

# Get user supplied values
imagePath = "./motion_images/autolock_motion.jpg"
cascPath = "haarcascade_frontalface_default.xml"
gap_sample_max=3
sleep_time_lock=3

def detectFace():
    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)

    # Read the image
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
        #flags = cv2.CV_HAAR_SCALE_IMAGE
    )
    #print "Found {0} faces!".format(len(faces))
    if len(faces) > 0:
        return True
    else:
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
    while True:
        # count = 0
        # while (count < 15):
        pic_time = os.path.getmtime(imagePath)
        logger.debug("pic_time is: %s" % pic_time)
        logger.debug("now      is: %s" % time.time())

        if pic_time == last_time and (pic_time + 15) >= time.time():
            gap_sample_cnt += 1
            if gap_sample_cnt >= gap_sample_max:
                is_face = detectFace()
                if not is_face:
                    gap_sample_cnt = 0
                    logger.debug("No faces, locking screen...")
                    os.system('setxkbmap us') #switch keyboard to US
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
