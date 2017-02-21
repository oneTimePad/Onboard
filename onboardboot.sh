#!/usr/bin/bash
HOMEDIR=$1


path="/home/"$HOMEDIR
vedir=$2


if [ ! -d $path"/pics" ]; then
	mkdir $path"/pics"
fi;

if [ ! -d $path"/telems" ]; then
	mkdir $path"/telems"
fi;
pictures=$path"/pics/pictures_"
telemfiles=$path"/telems/telemfiles_"
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
. $vedir"/onboard/bin/activate"
echo $pictures
echo $telemfiles
python $path"/Onboard/python/main.py" $3 $4 $pictures"/" $telemfiles"/"
