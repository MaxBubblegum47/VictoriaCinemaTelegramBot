# TofuFilm
Questo progetto è stato realizzato per l'esame di Algoritmi Distribuiti del secondo anno magistrale di Informatica, dipartimento FIM Unimore.

# Istruzioni per l'uso
Per fare funzionare il progetto devo lanciare questi comandi
```python
python -m Pyro4.naming
python tofu_server.py
python tofu_client.py
```
# Introduzione
Questo progetto prende spunto da un programma che avevo costruito anni fa la cui idea era quella di avere un bot Telegram in python per controllare che film fossero disponibili al cinema Victoria di Modena. Questo aveva funzionato egregiamente, ma avevo dismesso il progetto dopo qualche tempo perché impegnato con altre attività universitarie e non. Durante il corso di questo semestre, dovendo immaginare di creare una applicazione distribuita, ho pensato di rispolverare questa idea e di trasformarla in qualcosa di più artigianale e compliant con i requisiti del progetto. Ho eliminato completamente la parte del bot di telegram sostituendola con un server locale creato ad hoc.


Per portare a compimento il progetto ho fatto riferimento ad una libreria che permette di creare applicazioni distribuite o con modello client-server: Pyro4. Pyro è una libreria scritta interamente in Python che consente di costruire applicazioni in cui gli oggetti possono comunicare tra loro sulla rete ed è possibile farlo utilizzando i metodi python come siamo abituati a farlo, con quasi ogni tipo di parametro e valore di ritorno, mentre Pyro si occupa di individuare l'oggetto giusto sul computer corretto al fine di eseguire il metodo. 


Durante lo sviluppo di questa applicazione ho deciso di sostituire l'interfaccia di Telegram con una libreria grafica python: tkinter. Del vecchio progetto sono stati mantenuti i metodi di scraping, ma sono stati aggiornati: prima questi salvavano tutto su file statici testuali sfruttando la libreria pickle, mentre ora utilizzo un database dedicato ai film per poter salvare tutte le informazioni raccolte durante lo scraping. 


I requisiti del progetto sono i sequenti:
* Client
* * visualizzazione della programmazione settimanale dei film in sala o in specifici giorni scelti
* * consultazione listino prezzi ed informazioni rispetto ad eventuali scontistiche
* * visualizzazione sinossi e trailer, ove presenti, rispetto ai film in sala
* * possibilita' di scaricare un documento locale con all'interno tutta la programmazione settimanale delle proiezioni
* *  interazione con il programma tramite GUI
* * richiesta di update delle informazioni contenute nel server: il client deve poter chiedere al server di effettuare un aggiornamento delle informazioni
* *  registrazioni utenti al server
* *  creazione di lista dei film preferiti (per utente)
  
* Server
  
* * fornire al client tutte le informazioni necessarie rispetto alla programmazione dei film e loro sinossi/trailer
* *  operazioni di scraping al fine di ottenere tutte le informazioni utili al client
* *  mantenimento di una copia locale delle informazioni che si sono ottenute più di recente. Questo perche' qualora il sito da cui fare scraping non fosse piu' disponibile ci sarebbe comunque una copia  consultabile delle ultime informazioni raccolte.
* * storage degli utenti registrati/liste di film preferiti

Durante la fase finale di sviluppo è stata inoltre aggiunta una chat che permette agli utenti che hanno aperta una istanza del programma client, di poter comunicare con gli altri utenti che utilizzano l'applicazione.