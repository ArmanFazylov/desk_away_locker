#!/bin/bash
# Shantz Webcam Autolocker

stop_motion=`sudo pkill -f motion`
run_motion=`sudo motion -c motion.conf start`
`echo $stop_motion`
sleep 3
`echo $run_motion`
sleep 3
motion_pid=$(ps aux | grep motion | grep -v grep | awk '{print $2}')
echo "pid: $motion_pid"

gap_sample_cnt=0
gap_sample_max=3
sleep_time_lock=2

echo "$motion_sample_max $gap_sample_max $sleep_time_lock $sleep_time_unlock"

wm=`printenv | grep GNOME_DESKTOP_SESSION_ID`
if [ -n "$wm" ]
then
lock_cmd="gnome-screensaver-command -l"
unlock_cmd="gnome-screensaver-command -d"
else
lock_cmd="xscreensaver-command -l"
unlock_cmd="xscreensaver-command -d"
fi

facedetect_cmd=`python detect.py ./motion_images/autolock_motion.jpg haarcascade_frontalface_default.xml | sed -n '1!p'`

pic_time=0
last_time=0

while [ 1 ]
do
	pic_time=`date +%s -r motion_images/autolock_motion.jpg`
	pic_age=$(($pic_time + 30))
	now=`date +%s`

	echo "pictime $pic_time"
	echo "picage $pic_age"
	echo "now $now"

	# if no movement detected then start lock (gap) count
	if [ $pic_time -eq $last_time ] && [ $pic_age -ge $now ]
	then
	gap_sample_cnt=`expr $gap_sample_cnt + 1`
	echo "increment gap $gap_sample_cnt"
	# if samples reached critical point -> lock screen given there are no faces
	# else (there is a face) reset gap-count
	if [ $gap_sample_cnt -ge $gap_sample_max ]
	then
	result=$facedetect_cmd
	echo "$result"
	if [ $result -eq 0 ] || [ "$result" == "0"]; then
	echo "no face -> locking!"
	`echo $lock_cmd`
	gap_sample_cnt=0
	fi
	fi
	else
	# there is a motion
	gap_sample_cnt=0
	echo "there is a motion...doing nothing"
	fi

	sleep $sleep_time_lock

	last_time=$pic_time
done
