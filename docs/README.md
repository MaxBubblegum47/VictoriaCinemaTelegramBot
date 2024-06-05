# Relazione
## Descrizione del Progetto
Il progetto consiste in un bot telegram scritto in linguaggio python che permette la visualizzazione dei film disponibili nel cinema più famoso di Modena: il cinema Victoria (https://www.victoriacinema.it/victoria_cinema/index.php). Aprendo la chat con il bot e' possibile ottenere informazioni rispetto ai film che sono attualmente proiettati ed altri dettagli rispetto ai prezzi e convenzioni del cinema. 

Il programma è si articola in diverse componenti:
- bot telegram: main.py
- file di configurazione contenente il token per l'esecuzione del bot: config.py
- lo script che raccoglie informazioni rispetto ai film: movie.py
- file contenente informazioni aggiuntive rispetto al cinema: info.py
- orchestratori bash che permettono l'esecuzione continua di tutto il bot: main.sh, helper_main.sh, helper_movie.sh

Gli orchestratori gestiscono tutte le varie parti del bot e ciclicamente eseguono controlli sul sito per aggiornare i dati rispetto ai film disponibili.

## Preparazione
Per iniziare è necessario verificare di aver installato python all'interno del proprio computer. In base al sistema operativo che state attualmente utilizzando dovrete seguire una delle due seguenti guide.

### Unix (Linux/MacOS)
Aprire un terminale (bash/zsh) e digitare il seguente comando: `python3 --version`. Qualora venisse visualizzato a schermo un errore del tipo `command not found`, bisogna provvedere all'installazione di python3 all'interno del proprio dispositivo. A tal proposito rimandiamo alle seguenti guide:
- https://docs.python-guide.org/starting/install3/osx/
- https://docs.python-guide.org/starting/install3/linux/

### Windows 10/11
In maniera similare a quanto fatto su dispositivi Unix, anche in questo caso dobbiamo aprire un terminale, ma questa volta Powershell e digitare `python.exe --version`. Qualora venisse visualizzato a schermo un errore `python.exe non riconosciuto`, dovremo provvedere ad installare la versione più recente di python. Per fare ciò si rimanda alla seguente guida:
- https://docs.python.org/3/using/windows.html

#### Informazioni per python
In base al sistema su cui state lavorando e' possibile che qualora proviate ad installare una libreria python con il comando `pip`, questi vi restituisca un messaggio in cui vi consiglia di creare un `virtual envirorment`. Al fine di effettuare tale operazione si consiglia la lettura del seguente articolo: https://realpython.com/python-virtual-environments-a-primer/#how-can-you-work-with-a-python-virtual-environment

### Installazione pre-requisiti
Al fine di poter eseguire localmente il programma risulta infine necessaria l'installazione di una serie di librerie python che potrebbero non essere già installato sul vostro dispositivo. Si consiglia a tal proposito di eseguire il seguente comando: `pip install -r requirements.txt`

Questi provvedera' all'installazione di tutte le librerie utili al corretto funzionamento del progetto. 

Qualora non aveste installato `pip` sul vostro dispositivo, si consigli di seguire la seguente guida su come installare pip sul proprio dispositivo:
- https://pip.pypa.io/en/stable/installation/

## Funzionamento del Progetto
Per poter utilizzare il progetto e' necessario eseguire il comando `bash main.sh`. In tale modo verrà eseguito lo script bash che ha il compito di eseguire, e coordinare, le diverse componenti che caratterizzano il progetto. Tali componenti verranno analizzate approfonditamente nei successivi capitoli. E' anche possibile eseguire le singole parti del progetto utilizzando il comando `python3 <nome file>`.

## Sviluppo
### Scraper
La parte iniziale del progetto è stata dedicata allo sviluppo dello scraper del sito web del cinema. L'obiettivo è stato: invidividuare le pagine web contenenti informazioni rispetto alla proiezione dei film e prezzi/convenzioni. Una volta individuate scaricate le pagine web (in formato html) di interesse, il passo successivo è stato l'analisi delle suddette pagine al fine di estrapolare contenuto utile. Questo contenuto informativo vedremo come poi verra' utilizzato all'interno della componente del bot per generare messaggi testuali all'interno della chat con l'utente.

Il file `movie.py` definisce innanzitutto la classe Film, come segue:
```
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
```
Tale classe serve a creare degli oggetti che rappresentaranno i film (con tutti i possibili attributi) che vengono individuati all'interno del codice html della pagina web. Per fare questo effettuare questa analisi si utilizza la funzione `web_scraping`:

```
    def web_scraping():
        url = "https://www.victoriacinema.it/victoria_cinema/index.php"

        try:
            body = requests.get(url)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        with open('website.html', 'wb+') as f:
            f.write(body.content)

```

La funzione scarica la pagina web del sito del cinema in cui sono presenti tutte le informazioni relative ai film che sono attualmente in sala e salva il codice all'interno di un file chiamato `website.html`. Dopo aver salvato il codice della pagina web questo viene aperto ed analizzato. Il codice del sito presenta i film presenti in sala divisi in due macro categorie: 
- even film
- odd film

L'analisi del codice html segue questa divisione e sono quindi presenti due funzioni che si occupano di ottenere informazioni rispetto a film "odd" e i film "even". Di seguito una porzione di codice relativa all'ottenimento di informazioni per film odd.

```
    def Odd_Movie():
        with open('website.html', 'rb') as f:
            soup = BeautifulSoup(f.read(), 'lxml')

        divsOdd = soup.find_all("div", class_="filmContainer oddFilm")
        messageOdd = ""

        result_list = []

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

            f = Film(title, direction, genere, duration, cast, time_slots, reservation, trailer)
            messageOdd = f.title + "\n" + f.direction + "\n" + f.genere + "\n" + f.duration + "\n" + f.cast + "\n" + "\nProiezioni:" + "".join(str("\n" + elem + ":\n") if elem.isalpha() else str(elem + "   ") for elem in f.time_slots) + "\n\n\nLink Prenotazione:\n" + f.reservation + "\n\n\nTrailer:" + f.trailer + "\n\n\n"
            result_list.append(messageOdd)
            now = datetime.now()
            print("Movie Odd searched at time: " + str(now))
```

Quello che avviene all'interno della funzione appena visualizzati è un'analisi di tutte le diverse classi del codice html che possono contentere contenuto informativo. Si salvano tutte le informazioni all'interno di variabili che successivamente vengono utilizzato per creare l'oggetto `f` di classe Film. 

Ai fini dell'analisi vengono utilizzati dei metodi che sono forniti da beatifoulsoup: `find` e `find_all`. Una volta trovate le informazioni utili rispetto alla proiezione dei film, si esegue la pulizia del contenuto informativo ottenuto dal codice html. Per effettuare tale operazione si utilizza il metodo: `stripped_strings`. Questo metodo è disponibile all'interno degli strumenti messi a disposizione da Beatifulsoup e permette di pulire il codice html estraendo solamente testo realtivo al contenuto informativo che ci interessa. 

Una volta ottenute tutte le informazioni utili, si compone il messaggio relativo ad uno specifico film e lo si salva all'interno di una lista che contiene tutti quanti i film appartenenti ad un determinato macro gruppo (even/odd). I messaggi che vengono generati vengono salvati all'internod di file di testo chiamati:
- saveEven.txt
- saveOdd.txt

### Bot
Il programma `main.py`, che si occupa del funzionamento del bot, accede a questi due files di testo e carica tutti i messaggi che successivamente verranno stampati all'interno della chat tra utente e bot. Le altre informazioni relative ai costi, convenzioni, ... sono inserite all'interno di `info.py`. Questo viene importato come modulo all'interno di `main.py` e se ne estrapolano le informazioni utili al componimento di messaggi che verranno visualizzati via chat.

Il bot risponde ai seguenti input da parte dell'utente:
- **\start** ---> il bot esordisce con un messaggio di benveuto all'interno della chat
- **\film** ---> attraverso il seguente comando vengono elencati i film che sono presenti attualmente all'interno del cinema
- **\prezzi** ---> con tale comando vengono mostrati i prezzi
- **\info** ---> con tale input vengono mostrate informazioni aggiuntive rispetto al cinema e all'acquisto di biglietti

Il codice che gestice il bot e' lasciato in calce:
```
@bot.message_handler(commands=['start'])
def send_greetings(message):
    bot.send_message(message.chat.id, greetings_text)


@bot.message_handler(commands=['film'])
def send_film(message):
    messageEvenLoad = []
    messageOddLoad = []

    # Load the information from the file
    with open('saveEven.txt', 'rb') as file:
        messageEvenLoad = pickle.load(file)

    with open('saveOdd.txt', 'rb') as file:
        messageOddLoad = pickle.load(file)

    for elem in messageEvenLoad:
        bot.send_message(message.chat.id, elem)

    for elem in messageOddLoad:
        bot.send_message(message.chat.id, elem)


@bot.message_handler(commands=['prezzi'])
def send_price(message):
    bot.send_message(message.chat.id, price_text)


@bot.message_handler(commands=['info'])
def send_info(message):
    bot.send_message(message.chat.id, info_text)


bot.infinity_polling()
```
Ogni funzione gestisce uno specifico comando ed il comando `bot.infinity_polling()` pone il bot in uno stato di perpetuo ascolto di possibili comandi da parte dell'utente. 

### Orchestratore Bash
Tutti i componenti visti fino ad ora vengono orchestrati da una serie di script bash. Sono presenti in totale 3 scripts: due di questi gestiscono rispettivamente `movie.py` e `main.py`, mentre il terzo invece gestisce gli script bash appena citati, fungendo da orchestratore. Di seguito il contenuto di `main.sh`

```
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

```

Ogni volta che `main.sh` viene lanciato si controllano che tutti i requisiti siano installati correttamente e se non vi sono alcun tipo di messaggi di testo pronti all'uso, allora si esegue l'operazione di scraping del sito. Se sono presenti messaggi pronti per essere utilizzati si esegue il bot. Ad ogni modo, dopo 3600 secondi, verrà eseguito l'update dei messaggi; questo comporta il dump delle informazioni utili dal sito.

Gli altri due file bash contengono solamente l'eseguzione dei file python che controllano:

```
#!/bin/sh

python3 main.py
```

Questo è `helper_main.py` e di seguito `helper_movie.py`:

```
#!/bin/sh

python3 movie.py
```
Si ricorda il lettore che per poter eseguire correttamente il bot e' necessario inserire la propria chiave API del bot telegram creato, all'interno del file `config.py`.

### Esecuzione Docker
All'interno del progetto sono presenti le istruzioni per la costruzione di una immagine docker. Qui in calce lascio i comandi che permettono all'utente di costruire tale immagine e di lanciarne l'esecuzione.

Il primo comando da modo di poter creare l'immagine docker, menter il secondo di eseguirla:
- `docker build -t my-bot-image .` (all'interno della cartella `CinemaBot/`)
- `docker run --name my-bot-container my-bot-image`

Qualora primo comando fosse gia' stato eseguito in precedenza bastera' eseguire il seguente comando:
- `docker run my-bot-container`

Si segnala che e' possibile verificare quali immagini docker siano presenti all'interno del sistema attraverso il comando: `docker images`.

Per poter effettuare l'aggiornamento (o il caricamento) dell'immagine docker su docker hub, e' necessario eseguire i seguenti comandi:
- docker login --username `your username`
- docker build . -t `your username`/victoriacinemabot:latest
- docker tag "tag from the build" `your username`/victoriacinemabot
- docker push `your username`/victoriacinemabot

## DevOps
Per quel che concerne lo sviluppo DevOps è stata implementata una pipeline CD/CI che prevede l'utilizzo di librerie per il controllo di qualità del codice python ed unit test di alcune funzionalità del codice. Al termine di queste procedure di controllo qualita' sul codice, viene eseguito il deploy automatico del programma su dockerhub. Per il controllo del codice viene utilizzata una libreria chiamata flake8 (https://www.flake8rules.com/). Questa effettua un'analisi statica del codice python sia in fase di push che di pull, dal branch principale del progetto. Prima di effettuare tale analisi vengono però installati tutti quanti i requisiti necessari al funzionamento del programma. Sono stati abilitati alcuni flag che permettono di ignorare alcuni errori di formattazione del testo. Questi sono legati ai messaggi che vengono stampati dal bot all'interno della chat con l'utente e quasi sempre generano errori con l'utilizzo di flake8.

Per quel che riguarda la parte di unitest è stata utilizzata la libreria pytest e sono stati svolti test relativi alle seguenti funzionalità:
- funzionamento del sito web in cui sono presenti le informazioni relative ai film
- ottenimento informazioni relative ai film presenti sul sito

Di seguito il codice python relativo ai test effettuati:
```
class MockResponse:
    def __init__(self, content):
        self.content = content


def mock_get(url):
    if "https://www.victoriacinema.it/victoria_cinema/index.php" in url:
        with open("website.html", "rb") as f:
            return MockResponse(f.read())
    else:
        return MockResponse(b"")


@pytest.fixture
def mock_requests(monkeypatch):
    monkeypatch.setattr("requests.get", mock_get)


def test_web_scraping(mock_requests):
    Film.web_scraping()
    assert "website.html" in os.listdir()


def test_odd_movie(mock_requests):
    messageOdd = Film.Odd_Movie()
    assert isinstance(messageOdd, list)
    assert messageOdd


def test_even_movie(mock_requests):
    messageEven = Film.Even_Movie()
    assert isinstance(messageEven, list)
    assert messageEven

```

Una volta superati i test si procede con l'ultima fase della pipeline: la creazione e pubblicazione dell'immagine docker privata su dockerhub. La scelta di pubblicare l'immagine docker come privata è dovuta al fatto che all'interno di essa è contenuta la chiave dell'API di telegram.
Di seguito il codice della pipeline CD/CI:
```
name: Pipeline VictoriaCinemaBot

on:
  push:
    branches:
      - master
      - main
  pull_request:
    branches:
      - master
      - main
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up python 3.10
      uses: actions/setup-python@v2
      with:
        python-version: 3.7
    
    - name: Install dependencies
      run: pip install -r src/requirements.txt
    
    - name: Run Test on Python code with flake8
      run: flake8 --ignore=E501,E121,E126 .
    
    - name: Run Pytest
      working-directory: src/
      run: pytest
      
  docker:
    runs-on: ubuntu-latest
    steps:
      -
        name: Set up QEMU
        uses: docker/setup-qemu-action@v3
      -
        name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      -
        name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: <your username>
          password: <your password>
      -
        name: Build and push
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: maxbubblegum/victoriacinemabot:latest
```

## Sviluppi Futuri
Al momento il programma non e' concepito per poter operare con Kubernetes, ma dato che questo si basa su diversi servizi (scraping e bot), sarebbe interessante poter gestire questi con un vero orchestratore. L'idea sarebbe quella di accantonare l'orchestratore bash e i suoi 2 collaboratori. 

Sarebbe necessario inoltre non avere piu' due funzioni distinte per `film odd` e `film even`, ma averne solamente una che effettui tutta quanta l'analisi del codice html. Questo per evitare di avere grandi porzioni di codice ripetuto all'interno di `movie.py`. 

Ritengo possa essere inoltre necessario introdurre una funzionalita' di scraping anche per quel che riguarda i prezzi e le convenzioni del cinema. Al momento queste operazioni sono "manauli" nel senso che, non esiste alcuno scraper, ma manualmente aggiorno il file info.py che contiene tutte queste informazioni.

In ultima istanza mi piacerebbe poter eseguire il bot all'interno di una board, quale Arduino R4 Wi-Fi o esp8266. Penso che con una versione ridotta di python e delle sue librerie (o sfruttando maggiormente quelle builtin) sarebbe possibile far eseguire il progetto in maniera piu' efficiente in termini di consumo energetico, ma anche di ottimizzazione del codice.

Lorenzo Stigliano,
Matricola 185534,
Informatica Magistrale 
