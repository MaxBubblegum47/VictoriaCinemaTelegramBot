'''
This is the code that handles the scraper. We have a Film class in the begging and it is used
for storing info about each film (title, cast, trailer, ...); all those information are then
used to create files in which the is a list of messages. Each of these messages is a film (with all its specs).

To do the scraping the script download the html page of the movie teather than it analysizes the html code and
extract all the infos. The script leverages on BeatifulSoup library in order to achieve this goal. 
'''
from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
import pickle

class Film:
    def __init__(self, title, direction, genere, duration, cast,
                 time_slots, reservation, trailer):
        self.title = title
        self.direction = direction
        self.genere = genere
        self.duration = duration
        self.cast = cast
        self.time_slots = time_slots
        self.reservation = reservation
        self.trailer = trailer

    # This method download the html page and save it into website.html
    def web_scraping():
        url = "https://www.victoriacinema.it/victoria_cinema/index.php"

        try:
            body = requests.get(url)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        with open('website.html', 'wb+') as f:
            f.write(body.content)

    # Odd_Movie open website.html and the start to check the div class that contains odd movies. Thanks
    # to find and find_all method it retrieves all the spces of each movie. All of this is done with loop
    # and at the end of each of them the new movie is appended to result_list. This is a list with all the movies
    # that need to be displayed to the final user
    def Odd_Movie():
        with open('website.html', 'rb') as f:
            soup = BeautifulSoup(f.read(), 'lxml')

        divsOdd = soup.find_all("div", class_="filmContainer oddFilm")
        messageOdd = ""

        # final return of the method, it contains the list of all the messages
        result_list = []

        # in this nested loop the script is checking for title, direction, genere, duration, cast, time,
        # reservation link and trailer link. 
        for div in divsOdd:
            idfilm = div.find_all("div", class_="scheda")
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

            # the reservation link is half static and half auto generated. Basically the beginning is the same
            # for every movie, the only thing that change is the idFilm value. The script scrapes this value before
            # and then merges it with the static reservation link.
            for div1 in divs3:
                reservation = "https://www.victoriacinema.it/generic/scheda.php?id=" + str(idfilm).strip("['']") + "&idcine=1760&idwt=5103#inside"

                try:
                    body = requests.get(reservation)
                    body_text = body.content
                except requests.exceptions.RequestException as e:
                    raise SystemExit(e)

                soup = BeautifulSoup(body_text, 'lxml')
                divTrailer = soup.find_all("a", class_="linkTrailer linkExt")
                subdivTrailer = re.findall('href="(.*)"', str(divTrailer))
                try:
                    trailer = subdivTrailer[0]
                except IndexError:
                    print("Index out range for testing")

                # trailer = subdivTrailer[0]

                divTitolo = div1.find("div", class_="titolo")
                for clean_strip in list(divTitolo.stripped_strings):
                    title += " " + clean_strip

                divRegia = div1.find("div", class_="regia")
                for clean_strip in list(divRegia.stripped_strings):
                    direction += "" + clean_strip

                divGenere = div1.find("div", class_="genere")
                for clean_strip in list(divGenere.stripped_strings):
                    genere += " " + clean_strip

                divDurata = div1.find("div", class_="durata")
                for clean_strip in list(divDurata.stripped_strings):
                    duration += " " + clean_strip

                divCast = div1.find("div", class_="cast")
                for clean_strip in list(divCast.stripped_strings):
                    cast += " " + clean_strip

            divs2 = div.find_all("ul", class_="orari")
            for div2 in divs2:
                for clean_strip in list(div2.stripped_strings):
                    time_slots.append(clean_strip)

            # At the end of the analysis the script creates the object f of Film class with all the attributes
            # that have been scraped before and then the message related with that film is generated. Once the messagge
            # is done it is added to result_list. For each movie that are scraped there is a print to check that everything
            # is okay and a timestamp
            f = Film(title, direction, genere, duration, cast, time_slots, reservation, trailer)
            messageOdd = f.title + "\n" + f.direction + "\n" + f.genere + "\n" + f.duration + "\n" + f.cast + "\n" + "\nProiezioni:" + "".join(str("\n" + elem + ":\n") if elem.isalpha() else str(elem + "   ") for elem in f.time_slots) + "\n\n\nLink Prenotazione:\n" + f.reservation + "\n\n\nTrailer:" + f.trailer + "\n\n\n"
            result_list.append(messageOdd)
            now = datetime.now()
            print("Movie Odd searched at time: " + str(now))

        return result_list

    # Read the comment inside Odd_Movie method, because it is essentially the same
    def Even_Movie():
        with open('website.html', 'rb') as f:
            soup = BeautifulSoup(f.read(), 'lxml')

        divsEven = soup.find_all("div", class_="filmContainer evenFilm")
        messageEven = ""
        result_list = []

        for div in divsEven:
            idfilm = div.find_all("div", class_="scheda")
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
            for div1 in divs3:

                reservation = "https://www.victoriacinema.it/generic/scheda.php?id=" + str(idfilm).strip("['']") + "&idcine=1760&idwt=5103#inside"

                try:
                    body = requests.get(reservation)
                    body_text = body.content
                except requests.exceptions.RequestException as e:
                    raise SystemExit(e)

                soup = BeautifulSoup(body_text, 'lxml')
                divTrailer = soup.find_all("a", class_="linkTrailer linkExt")
                subdivTrailer = re.findall('href="(.*)"', str(divTrailer))
                try:
                    trailer = subdivTrailer[0]
                except IndexError:
                    print("Index out range for testing")

                divTitolo = div1.find("div", class_="titolo")
                for clean_strip in list(divTitolo.stripped_strings):
                    title += " " + clean_strip

                divRegia = div1.find("div", class_="regia")
                for clean_strip in list(divRegia.stripped_strings):
                    direction += " " + clean_strip

                divGenere = div1.find("div", class_="genere")
                for clean_strip in list(divGenere.stripped_strings):
                    genere += " " + clean_strip

                divDurata = div1.find("div", class_="durata")
                for clean_strip in list(divDurata.stripped_strings):
                    duration += " " + clean_strip

                divCast = div1.find("div", class_="cast")
                for clean_strip in list(divCast.stripped_strings):
                    cast += " " + clean_strip

                body = requests.get(reservation)
                body_text = body.content
                soup = BeautifulSoup(body_text, 'lxml')
                divTrailer = soup.find_all("a", class_="linkTrailer linkExt")
                subdivTrailer = re.findall('href="(.*)"', str(divTrailer))
                try:
                    trailer = subdivTrailer[0]
                except IndexError:
                    print("Index out range for testing")

            divs2 = div.find_all("ul", class_="orari")
            for div2 in divs2:
                for clean_strip in list(div2.stripped_strings):
                    time_slots.append(clean_strip)

            f = Film(title, direction, genere, duration, cast, time_slots, reservation, trailer)
            messageEven = f.title + "\n" + f.direction + "\n" + f.genere + "\n" + f.duration + "\n" + f.cast + "\n" + "\nProiezioni:" + "".join(str("\n" + elem + ":\n") if elem.isalpha() else str(elem + "   ") for elem in f.time_slots) + "\n\n\nLink Prenotazione:\n" + f.reservation + "\n\n\nTrailer:" + f.trailer + "\n\n\n"
            result_list.append(messageEven)
            now = datetime.now()
            print("Movie Even searched at time: " + str(now))

        return result_list

# The main start the scraping (which dowloads the html page) and then start the analysis for odd
# and even movies inside the webpage. After that it takes the results from Odd_Movie and Even_Movie
# (result_list, that contains all the messages) and it saves them into two different files: 
# - saveEven.txt
# - saveOdd.txt
def main():
    Film.web_scraping()

    messageOdd = Film.Odd_Movie()
    messageEven = Film.Even_Movie()

    with open('saveEven.txt', 'wb') as file:
        pickle.dump(messageEven, file)

    with open('saveOdd.txt', 'wb') as file:
        pickle.dump(messageOdd, file)

if __name__ == "__main__":
    main()
