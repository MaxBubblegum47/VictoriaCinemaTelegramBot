# CinemaBot
CinemaBot is a little telegram bot that collects information from my local movie theater's website: https://www.victoriacinema.it/victoria_cinema/index.php and displays them as messages via telegram. There's a chat thanks to that you can interact with the bot and get this informatios:
* When they are in the theater
* Duration
* Cast
* Direction
* Genere
* Movie trailer
* Reservation link

## How does it work?
The first thigs is to create a file: _config.py_ and add the following line:

```python
TOKEN = "place your API key here"
BOTNAME = "place here the name of your bot"
```

Then, after installing the requirements with `pip install -r requirements.txt`, you can execute the following line:

```bash
bash main.sh
```

I want to remember you that now to use pip you need to create a virtual envirorment before.

### Available Commands
* film/start: shows all the film that are available on https://www.victoriacinema.it/victoria_cinema/index.php
* prezzi/price: shows ticket's prices
* info: shows all other infos (e.g. discount)

### Screenshots
![screenshot_1](https://user-images.githubusercontent.com/59342085/165149574-523d1478-945d-4156-9f17-e4c8f50d6c48.png)
![screenshot_2](https://user-images.githubusercontent.com/59342085/165149579-d7c0a80a-714f-4a25-ba7c-e32b699b8a2d.png)


### How it works?
The bot has two parts:
* bot
* movie updater

The aim of the bot is to display information to the user in the telegram chat, while the movie updater is responsible for retrieves information about the movies.

### About the website
The website was done by https://www.creaweb.it/creaweb/index.php 
The company that seems to create website (_php_ based) for movie theaters. It has curious html configurations, in which movies are divided in Even and Odd `div class`. 

### Information for the Developer
#### How to run the program
Simply do `bash main.sh`

#### How to push to docker hub
Commands list (**you need to change maxbubblegum wit your user**):
- docker login --username maxbubblegum
- docker build . -t maxbubblegum47/victoriacinemabot:latest
- docker tag "tag from the build" maxbubblegum/victoriacinemabot
- docker push maxbubblegum/victoriacinemabot

#### How to run the docker image
If you want to run the program without thinking to much about docker, just `CTRL + C CTRL + V` this two commands in your terminal:
- `docker build -t my-bot-image .` (in VictoriaCinema main folder)
- `docker run --name my-bot-container my-bot-image`

If for some reason you have done this in advance and now the terminal is telling you that this image exists yet, you can check it by using `docker images` to list all the possible images and the simply `docker run <name of the image>`.