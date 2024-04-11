# VictoriaCinemaBot
Little Bot that collects information from my local movie theater's website: https://www.victoriacinema.it/victoria_cinema/index.php and displays information about movies:
* When they are in the theater
* Duration
* Cast
* Direction
* Genere
* Movie trailer
* Reservation link

## How to make it works?
The first thigs to do is to create a file: _config.py_ and adding the following line:
```python
TOKEN = "place your API key here"
BOTNAME = "place here the name of your bot"
```
Then, after installing the requirements (I auto generated it with _pipreqs_), you can execute the following line:
```bash
bash container.sh
```
Note that: in all bash scripts I used _python3_ as python command. Make sure that your system has this command available, otherwise the script may not works at all.

### Available Commands
* film/start: display all the film that are available on https://www.victoriacinema.it/victoria_cinema/index.php
* prezzi/price: shows movie's ticket price
* info: show all other information related with the movie theater

### Screenshots
![screenshot_1](https://user-images.githubusercontent.com/59342085/165149574-523d1478-945d-4156-9f17-e4c8f50d6c48.png)
![screenshot_2](https://user-images.githubusercontent.com/59342085/165149579-d7c0a80a-714f-4a25-ba7c-e32b699b8a2d.png)


### How it works?
The bot has two parts:
* bot itself
* movie updater

The first aim to display information to the user every time he presses the button on the telegram chat. The movie updater is responsible for retrieves the movies information (once every hour) and saving them into files. I handle both with a _containter_ written in _bash_. It makes run the updater once per hour and keep alive the bot.

### About the website
The website is done by https://www.creaweb.it/creaweb/index.php, a company that seems to create website (_php_ based) for movie theaters. It has curious html configurations, in which movies are divided in Even and Odd, so I had two to write similar funcion to catch the _even movies_ and the _odd_ ones. Then I put everything into two differnts list (_even, odd_) saving everything in files. The bot open the right file (even one or the odd one), read the content and print movie's information to the user. I dump just one time the hrml webpage then I start to analyze it.

##### About messy commits
I did a wrong commit, committing something like 4 file at once, but I'm lazy so I don't think I'm gonna fix it for now :(


#### How to push to docker
Commands list:
- docker login --username maxbubblegum
- docker build . -t maxbubblegum47/victoriacinemabot:latest
- docker tag "tag from the build" maxbubblegum/victoriacinemabot
- docker push maxbubblegum/victoriacinemabot