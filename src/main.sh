#!/bin/sh

pip3 install -r requirements.txt

if [[ -f 'saveEven.txt' ]] & [[ -f 'saveOdd.txt' ]]
then
	echo "Save files are present. I'm starting the bot."
	bash helper_main.sh &
else
	echo "There are not save files available. I'm collecting information about movies"
	bash helper_movie.sh	
fi



while true
do
	echo "Starting the bot..."
	bash helper_main.sh
	sleep 3600
	echo "Updating Movies"
	bash helper_movie.sh	
done
