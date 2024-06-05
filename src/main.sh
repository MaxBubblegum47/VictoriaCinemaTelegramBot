#!/bin/sh

# install all the requirements before starting
pip3 install -r requirements.txt

# check if messages's files are available, if not create them with the helper_main.sh
if [[ -f 'saveEven.txt' ]] & [[ -f 'saveOdd.txt' ]]
then
	echo "Save files are present. I'm starting the bot."
	bash helper_main.sh &
else
	echo "There are not save files available. I'm collecting information about movies"
	bash helper_movie.sh	
fi

# run the bot until the end of time
while true
do
	echo "Starting the bot..."
	bash helper_main.sh
	sleep 3600
	echo "Updating Movies"
	bash helper_movie.sh	
done
