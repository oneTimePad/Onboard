#!/usr/bin/bash

path="/home/ruautonomous/"

if [ ! -d $path"/pics" ]; then
	mkdir $path"/pics"
fi;

if [ ! -d $path"/telems" ]; then
	mkdir $path"/telems"
fi;
pictures=$path"pics/pictures_"
telemfiles=$path"telems/telemfiles_"
rand=$RANDOM
tmppics=""
tmptelems=""
tmppics=$pictures$rand
tmptelems=$telemfiles$rand
while [ -d $tmppics ] || [ -d $tmptelems ]; do
	rand=$RANDOM
	tmppics=$pictures$rand
	tmptelems=$telemfiles$rand
done
pictures=$tmppics
telemfiles=$tmptelems

mkdir $pictures 
mkdir $telemfiles
. /home/ruautonomous/.virtualenvs/onboard/bin/activate

python /home/ruautonomous/Onboard/python/main.py 192.168.123.200 8443 $pictures $telemfiles
