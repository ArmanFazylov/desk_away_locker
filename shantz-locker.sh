#!/bin/bash
# Shantz Webcam Autolocker
# A simple, useless script to monitor motion in front of your PC, autolock it when you are away and autounlock it when you come back.
# Kinda useless cuz there is no security and any kind of motion triggers the unlock. 
# But still if you like it, then give me a shout at http://tech.shantanugoel.com or http://blog.shantanugoel.com
# The home page for this script is at http://tech.shantanugoel.com/shantz-webcam-autolocker

#Usage: ./shantz-locker [-l <LockThreshold>] [-u UnlockThreshold] [-s LockScanInterval] [-t UnlockScanInterval]
#LockThreshold - Determines the threshold (based on no. of samples sans motion) to lock your PC. Default is 5
#UnlockThreshold - Determines the threshold (based on no. of samples with motion) to unlock your PC. Default is 2
#LockScanInterval - How soon to check if there is motion when your PC is in unlocked state. Default interval is 5 seconds
#UnlockScanInterval - How soon to check if there is motion when your PC is in locked state. Default interval is 2 seconds


motion_sample_cnt=0
motion_sample_max=2
gap_sample_cnt=0
gap_sample_max=5
sleep_time_lock=1
sleep_time_unlock=2

while getopts "l:u:s:t:" flag
do
    case $flag in
    l)  echo "Updating Lock Threshold to $OPTARG"
        gap_sample_max=$OPTARG
        ;;
    u)  echo "Updating Unlock Threshold to $OPTARG"
        motion_sample_max=$OPTARG
        ;;
    s)  echo "Updating Lock Scan Interval to $OPTARG"
        sleep_time_lock=$OPTARG
        ;;
    t)  echo "Updating Unlock Scan Interval to $OPTARG"
        sleep_time_unlock=$OPTARG
        ;;
    ?) printf "Usage: %s [-l <LockThreshold>] [-u UnlockThreshold] [-s LockScanInterval] [-t UnlockScanInterval]\n" >&2
        exit 2
        ;;
    esac
done
#echo "$motion_sample_max $gap_sample_max $sleep_time_lock $sleep_time_unlock"

wm=`printenv | grep GNOME_DESKTOP_SESSION_ID`
if [ -n "$wm" ]
then
lock_cmd="gnome-screensaver-command -l"
unlock_cmd="gnome-screensaver-command -d"
else
lock_cmd="xscreensaver-command -l"
unlock_cmd="xscreensaver-command -d"
fi
facedetect_cmd=`python ./facedetect/detect.py /home/arman/Projects/motion_images/autolock_motion.jpg ./facedetect/haarcascade_frontalface_default.xml`

state=0
curr_time=0
last_time=0
#0 is unlocked 1 is locked

while [ 1 ]
do
	curr_time=`date +%s -r motion_images/autolock_motion.jpg`
	if [ $curr_time -eq $last_time ]
	then
	gap_sample_cnt=`expr $gap_sample_cnt + 1`
	#echo "increment gap $gap_sample_cnt"
	else
	motion_sample_cnt=`expr $motion_sample_cnt + 1`
	#echo "increment motion $motion_sample_cnt"
	fi
	
	if [ $gap_sample_cnt -ge $gap_sample_max ]
	then
	gap_sample_cnt=0
	motion_sample_cnt=0
	if [ $state == 0 ]
	then
	result=$facedetect_cmd
	if [ $result -eq 0 ] 
	then
	state=1
	`echo $lock_cmd`
	fi
	#else
	#echo "reset motion ctr"
	fi
	fi

	if [ $motion_sample_cnt -ge $motion_sample_max ]
	then
	motion_sample_cnt=0
	gap_sample_cnt=0
	if [ $state == 1 ]
	then
	state=0
	`echo $unlock_cmd`
	#else
	#echo "reset gap ctr"
	fi
	fi
	
	if [ $state == 0 ]
	then
	sleep $sleep_time_lock
	#echo $sleep_time_lock
	else
	sleep $sleep_time_unlock
	#echo $sleep_time_unlock
	fi

	last_time=$curr_time
done
