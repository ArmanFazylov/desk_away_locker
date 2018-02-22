## DESK AWAY LOCKER

At work we have a prank to install browser extension which replaces all images to Nicolas Cage (see nCage: https://goo.gl/rTl496) whenever any of us leaves the desk computer unattended. Because of that, I always need to lock my screen even when I am going to washroom. Remembering to press lockscreen keyboard combination is cumbersome, so I decided to build this project. It is mostly based on this two projects (Shantanu's webcam autolocker https://goo.gl/Cq5cHa and Shantnu Tiwari's Face Recognition with Python https://goo.gl/1YFKvM). 
Project is still raw, however accomplishes the purpose.

### Prerequisites
1. Linux (mine is Ubuntu 16.04 )
2. Motion software 
```sh
sudo apt-get install motion
```
3. OpenCV software (tedious process, but there is a well written guide https://goo.gl/PC10Rl)

### Steps
1. Clone repo
2. In file motion.conf:

Change daemon to 'on' ( to run motion as daemon)
```sh
daemon on
```
Run below command to check webcam names on the computer
```sh
$ ls -ltrh /dev/video*
```
Since I am using USB webcam, I am using  /dev/video1
Change value to the preferred camera
```sh
videodevice /dev/video1
```
Change input config
```sh
input -1
```

3. Enter your python environment (as per guide https://goo.gl/PC10Rl)
```sh
$ workon cv
```
4. Run bash_script (make sure it is executable)
```sh
(cv) $ nohup python locker.py &
```
5. Enjoy ur privacy)


### How it works
Basically, (locker.py) upon detected motion creates file 'motion_images/autolock_motion.jpg'. Then, face recognition command is run to detect if the newly created autolock_motion.jpg picture has a face on it. If it doesn't - it means that user left the desk (i.e. picture of a chair or a wall). So the screen is locked. 
Feel free to to add improvements.


### Future
I am planning to go one step further, and lock screen based on face recognition --- lock screen if person is not me))
