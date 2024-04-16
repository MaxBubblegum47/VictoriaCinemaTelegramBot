from time import time
from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
from db import db_insert, db_test
import os

def delete_old_db():
    os.remove('movies.db')

def web_scraping():
    url = "https://www.victoriacinema.it/victoria_cinema/index.php"
    
    try:
        body = requests.get(url)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)
    
    with open('website.html', 'wb+') as f:
        f.write(body.content)    

def Odd_Movie():

    with open('website.html', 'rb') as f:
        soup = BeautifulSoup(f.read(), 'lxml')

    divsOdd = soup.find_all("div", class_="filmContainer oddFilm")
    # old variables for the old way of scraping without db
    messageOdd = ""
    result_list = []
    #oddFilm loop
    for div in divsOdd:
        idfilm = div.find_all("div",  class_="scheda")
        idfilm = re.findall(r"\D(\d{5})\D", str(idfilm))
        title = ""
        direction = ""
        genere = ""
        duration = ""
        cast = ""
        time_slots = []
        reservation = ""
        trailer = ""
        divs3 = div.find_all("div", class_="datiFilm")
        #Film data
        for div1 in divs3:
            # getting reservation link
            reservation = "https://www.victoriacinema.it/generic/scheda.php?id=" + str(idfilm).strip("['']") + "&idcine=1760&idwt=5103#inside"
            
            try:
                body = requests.get(reservation)
                body_text = body.content
            except requests.exceptions.RequestException as e:
                raise SystemExit(e)
            # getting trailer link
            soup = BeautifulSoup(body_text, 'lxml')     
            divTrailer = soup.find_all("a", class_="linkTrailer linkExt")
            subdivTrailer = re.findall('href="(.*)"', str(divTrailer))
            trailer = subdivTrailer[0]
            # handling title
            divTitolo = div1.find("div", class_="titolo")
            for clean_strip in list (divTitolo.stripped_strings):
                title += " " + clean_strip
            divRegia = div1.find("div", class_="regia")
            for clean_strip in list (divRegia.stripped_strings):
                direction += "" + clean_strip
            divGenere = div1.find("div", class_="genere")
            for clean_strip in list (divGenere.stripped_strings):
                genere += " " + clean_strip
            divDurata = div1.find("div", class_="durata")
            for clean_strip in list (divDurata.stripped_strings):
                duration += " " + clean_strip
            divCast = div1.find("div", class_="cast")
            for clean_strip in list (divCast.stripped_strings):
                cast += " " + clean_strip
        #getting the day and the time for each film in the theater
        divs2 = div.find_all("ul", class_="orari")
        for div2 in divs2:
            for clean_strip in list(div2.stripped_strings):
                time_slots.append(clean_strip)
        
        # old way of adding film to a list and then print all as a message on telegram
        # # adding film to the list and preparing updating message
        # f = Film(title, direction, genere, duration, cast, time_slots, reservation, trailer)
        # messageOdd = f.title + "\n" + f.direction + "\n" + f.genere + "\n" + f.duration + "\n" + f.cast + "\n" + "\nProiezioni:" + "".join(str("\n" + elem + ":\n") if elem.isalpha() else str(elem + "   ") for elem in f.time_slots )+ "\n\n\nLink Prenotazione:\n" + f.reservation +"\n\n\nTrailer:" + f.trailer +"\n\n\n"            
        db_insert(title, direction, genere, duration, cast, time_slots, reservation, trailer)
        # result_list.append(messageOdd)
        
        now = datetime.now()
        
        print("Movie Odd searched at time: " + str(now))
        
        # quick check
        # print(f.title)
    
    return 0

def Even_Movie():

    with open('website.html', 'rb') as f:
        soup = BeautifulSoup(f.read(), 'lxml')

    divsOdd = soup.find_all("div", class_="filmContainer evenFilm")
    messageOdd = ""
    result_list = []
    #oddFilm loop
    for div in divsOdd:
        idfilm = div.find_all("div",  class_="scheda")
        idfilm = re.findall(r"\D(\d{5})\D", str(idfilm))
        title = ""
        direction = ""
        genere = ""
        duration = ""
        cast = ""
        time_slots = []
        reservation = ""
        trailer = ""
        divs3 = div.find_all("div", class_="datiFilm")
        #Film data
        for div1 in divs3:
            # getting reservation link
            reservation = "https://www.victoriacinema.it/generic/scheda.php?id=" + str(idfilm).strip("['']") + "&idcine=1760&idwt=5103#inside"
            
            try:
                body = requests.get(reservation)
                body_text = body.content
            except requests.exceptions.RequestException as e:
                raise SystemExit(e)
            # getting trailer link
            soup = BeautifulSoup(body_text, 'lxml')     
            divTrailer = soup.find_all("a", class_="linkTrailer linkExt")
            subdivTrailer = re.findall('href="(.*)"', str(divTrailer))
            trailer = subdivTrailer[0]
            # handling title
            divTitolo = div1.find("div", class_="titolo")
            for clean_strip in list (divTitolo.stripped_strings):
                title += " " + clean_strip
            divRegia = div1.find("div", class_="regia")
            for clean_strip in list (divRegia.stripped_strings):
                direction += "" + clean_strip
            divGenere = div1.find("div", class_="genere")
            for clean_strip in list (divGenere.stripped_strings):
                genere += " " + clean_strip
            divDurata = div1.find("div", class_="durata")
            for clean_strip in list (divDurata.stripped_strings):
                duration += " " + clean_strip
            divCast = div1.find("div", class_="cast")
            for clean_strip in list (divCast.stripped_strings):
                cast += " " + clean_strip
        #getting the day and the time for each film in the theater
        divs2 = div.find_all("ul", class_="orari")
        for div2 in divs2:
            for clean_strip in list(div2.stripped_strings):
                time_slots.append(clean_strip)
        # # adding film to the list and preparing updating message
        # f = Film(title, direction, genere, duration, cast, time_slots, reservation, trailer)
        # messageOdd = f.title + "\n" + f.direction + "\n" + f.genere + "\n" + f.duration + "\n" + f.cast + "\n" + "\nProiezioni:" + "".join(str("\n" + elem + ":\n") if elem.isalpha() else str(elem + "   ") for elem in f.time_slots )+ "\n\n\nLink Prenotazione:\n" + f.reservation +"\n\n\nTrailer:" + f.trailer +"\n\n\n"            
        db_insert(title, direction, genere, duration, cast, time_slots, reservation, trailer)
        # result_list.append(messageOdd)
        
        now = datetime.now()
        
        print("Movie Even searched at time: " + str(now))

def getting_info():
    replacers = {'</div>' : ' ', '<strong>' : ' ', '</span>' : ' ', '</strong>' : ' ', 
                 '<br/>' : ' ', '</a>' : ' '}

    url = "https://www.victoriacinema.it/victoria_cinema/prezziecard.php"
    
    try:
        body = requests.get(url)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)
    
    with open('film_info.html', 'wb+') as f:
        f.write(body.content) 
    
    with open('film_info.html', 'rb') as f:
        soup = BeautifulSoup(f.read(), 'lxml')
    
    divsOdd = soup.find_all("div", class_="priceTab_row cleared odd")
    divsEven = soup.find_all("div", class_="priceTab_row cleared even")

    resOdd = str(divsOdd)
    resOdd = re.findall('>([^"]*)<', resOdd) # the power of regex

    listOdd = []

    for elem in resOdd:
        listOdd.append(elem.replace('</div>', ' ').replace('<strong>', ' ').replace('</span>', ' ').replace('</strong>', ' ').replace('<br/>', ' ').replace('</a>', ' ')) # I know it is really ugly, but it is working fine and the dict wan not working properly

    resEven = str(divsEven)
    resEven = re.findall('>([^"]*)<', resEven) # the power of regex

    listEven = []

    for elem in resEven:
        listEven.append(elem.replace('</div>', ' ').replace('<strong>', ' ').replace('</span>', ' ').replace('</strong>', ' ').replace('<br/>', ' ').replace('</a>', ' ')) # I know it is really ugly, but it is working fine and the dict wan not working properly

    return listOdd, listEven

def main():
    web_scraping()
    Even_Movie()
    Odd_Movie()
    db_test()
    getting_info()

if __name__ == "__main__":
    main()
