DESK AWAY LOCKER

At work we have a prank to install browser extension which replaces all images to Nicolas Cage (see nCage: https://goo.gl/rTl496) whenever any of us leaves the desk computer unattended. Because of that, I always need to lock my screen even when I am going to washroom. Remembering to press lockscreen keyboard combination is cumbersome so I decided to build this project. Basically, this program locks screen whenever I leave my desk. It is mostly based on this two projects (Shantanu's webcam autolocker https://goo.gl/Cq5cHa and Shantnu Tiwari's Face Recognition with Python https://goo.gl/1YFKvM). 
Project is raw, however accomplishes the purpose.


Prerequisites
1. Linux (mine is Ubuntu 16.04 )
2. Motion software (sudo apt-get install motion)
3. OpenCV software (tedious process, but there is a well written guide https://goo.gl/PC10Rl)


Steps
1. Clone repo
2. In file motion.conf 
	2.1 Change this to 'on' (in order to run motion as daemon)
		daemon off
	2.2 Run this command to check webcam names on the computer
			ls -ltrh /dev/video*
   		Since I am using USB webcam, I am using  /dev/video1
   		Change value to the preferred camera
   			videodevice /dev/video1
   		Change input config
   			input -1		

3. In shantz-locker.sh script, change paths to the ones on your machine
	facedetect_cmd=`python ./facedetect/detect.py /home/arman/Projects/motion_images/autolock_motion.jpg ./facedetect haarcascade_frontalface_default.xml`

4. Run motion (don't forget to plug in USB camera)
	cd ~/Projects/desk_away_locker
	sudo service motion -c motion.conf start

5. Enter your python environment (as per guide https://goo.gl/PC10Rl)
	workon cv

6. Run bash_script 
	./shantz-locker.sh

7. Enjoy ur privacy)


How it works
Basically, shantz-locker.sh script upon detected motion creates file motion_images/autolock_motion.jpg.
Then, python script is run to detect if the newly created autolock_motion.jpg picture has a face on it. If it doesn't, the screen is locked.

Feel free to to add improvements.


Future
I am planning to go one step further, and lock screen based on face recognition --- lock screen if person is not me))