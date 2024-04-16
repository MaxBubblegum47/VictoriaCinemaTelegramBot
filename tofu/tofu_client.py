import tkinter as tk
from tkinter import ttk
from tkinter import *
import Pyro4
import hashlib
from subprocess import call
import threading
from PIL import ImageTk, Image

class tofu(tk.Frame):
    def __init__(self, root):
        root.geometry("2000x850")

        # create Treeview with 3 columns
        cols = ('N.', 'Title', 'Direction', 'Genre', 'Duration')
        self.listBox = ttk.Treeview(root, columns=cols, selectmode='browse', show='headings') # one day I need to change it into a real listbox
        self.listBox.pack(side='right', fill='y')

        # title and logo
        root.title("TofuFilm")
        im = Image.open('sleepykirby.jpg')
        photo = ImageTk.PhotoImage(im)
        root.wm_iconphoto(True, photo)

        # Create a Scrollbar
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.listBox.yview)
        self.listBox.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")

        # it is listbox but it is actually a treeview
        self.listBox.column("N.", width=50)
        self.listBox.column("Title", width=600)
        self.listBox.column("Direction", width=350)
        self.listBox.column("Genre", width=350)
        self.listBox.column("Duration", width=220)

        # fonts
        style = ttk.Style()
        style.configure(".", font=("Arial",25), foreground="white")
        style.configure("Treeview.Heading", font=("Arial",25), foreground="white")
        style.configure("Treeview", foreground='black')
        style.configure("Treeview.Heading", foreground='black') #<----
        style.configure('Treeview', rowheight=40)

        # gestione della scelta del giorno
        options = [ 
            "Tutti",
            "Lunedì", 
            "Martedì", 
            "Mercoledì", 
            "Giovedì", 
            "Venerdì", 
            "Sabato", 
            "Domenica",
            "n.d."
        ] 
        # datatype of menu text 
        self.clicked = StringVar() 
        # initial menu text 
        self.clicked.set( "Tutti" ) 
        # Create Label for day
        self.label = Label( root , text = "" )  

        # set column headings
        for col in cols:
            self.listBox.heading(col, text=col)    

        # film favourite list 
        self.favourites_list = []

        # label to display into main window
        self.T1 = Text(root, height = 5, width = 52)
        self.l1 = Label(root, text = "username")
        self.l1.config(font =("Arial",25))

        self.T2 = Text(root, height = 5, width = 52)
        self.l2 = Label(root, text = "password")
        self.l2.config(font =("Arial",25))

        self.T1.pack()
        self.T2.pack()

        self.l1.pack()
        self.l2.pack()

        # default label for user
        self.login_label = Label(root, text = "utente")
        self.login_label.config(font =("Arial",25))
        self.login_label.pack()

        # old buttons
        # self.ApplyDayButton = tk.Button(root , text = "Applica giorno" , command = self.choose_day, font=("Arial",25)).pack(side='top', fill='x') # show film with particualr day
        # self.PrintUser = tk.Button(root, text = 'Printuser', command = tofu.print_all_user,font=("Arial",25)).pack(side='top', fill='x')
        # self.Login_Register_Button = tk.Button(root, text = 'Login/Register', command = tofu.login_register_window,font=("Arial",25)).pack(side='top', fill='x')    
        
        # buttons
        self.showroot = tk.Button(root, text="Mostra Film", width=15, command=self.show_all, font=("Arial",25))
        self.showroot.pack(side='top', fill='x') # show all film
        self.time = tk.Button(root, text="Info", width=15, command=self.show_info, font=("Arial",25))
        self.time.pack(side='top', fill='x') # show times slots for film
        self.InfoPrices = tk.Button(root, text = 'Info Prezzi', command = self.show_info_prices,font=("Arial",25))
        self.InfoPrices.pack(side='top', fill='x')
        self.closeButton = tk.Button(root, text="Chiudi", width=15, command=lambda:[root.destroy, self.kill_threads], font=("Arial",25))
        self.closeButton.pack(side='bottom') # close the app
        self.drop = tk.OptionMenu(root , self.clicked , *options)
        self.drop.pack(side='top', fill='x') # choice menu with days
        self.RefreshButton = tk.Button(root, text = 'Aggiorna Database', command = self.db_update,font=("Arial",25))
        self.RefreshButton.pack(side='top', fill='x')
        self.DumpButton = tk.Button(root, text = 'Dump Database', command = self.dump_treeview,font=("Arial",25))
        self.DumpButton.pack(side='top', fill='x')
        self.RegisterButton = tk.Button(root, text = 'Register', command = self.register,font=("Arial",25))
        self.RegisterButton.pack(side='top', fill='x')
        self.LoginButton = tk.Button(root, text = 'Login', command = self.login,font=("Arial",25))
        self.LoginButton.pack(side='top', fill='x')
        self.AddFavourite = tk.Button(root, text = 'Add Favourites', command = self.add_favourites,font=("Arial",25))
        self.AddFavourite.pack(side='top', fill='x')
        self.UpdateFav = tk.Button(root, text = 'Update Favourites', command = self.update_favourites,font=("Arial",25))
        self.UpdateFav.pack(side='top', fill='x')
        self.DumpFv = tk.Button(root, text = 'Dump Favourites List', command = self.dump_favourites_list,font=("Arial",25))
        self.DumpFv.pack(side='top', fill='x')
        self.FilmChat = tk.Button(root, text = 'Chat', command = self.film_chat,font=("Arial",25))
        self.FilmChat.pack(side='top', fill='x')

    # inserting all the film inside the treeview
    def show_all_helper(self):
        greeting_maker = Pyro4.Proxy("PYRONAME:example.greeting")
        rows = greeting_maker.get_film()

        self.listBox.delete(*self.listBox.get_children())

        for i, elem in enumerate(rows, start=0):
            self.listBox.insert("", tk.END, values=(i, elem[0], elem[1], elem[2], elem[3], elem[4], elem[5]))
        
    def show_all(self):
        self.listBox.delete(*self.listBox.get_children())

        greeting_maker = Pyro4.Proxy("PYRONAME:example.greeting")
        rows = greeting_maker.get_film()

        self.label.config( text = self.clicked.get() ) 
        day = self.label.cget('text')

        if day == 'Tutti':
            self.show_all_helper()
            return

        for i, elem in enumerate(rows, start=0):
            if day in str(elem):
                self.listBox.insert("", "end", values=(i, elem[0], elem[1], elem[2], elem[3], elem[4], elem[5]))

    # create a windows to dissaply all informations about film 
    def show_info(self):
        curItem = self.listBox.focus()
        newWindow = tk.Tk()

        # sets the title of the
        # Toplevel widget
        newWindow.title("Info")
    
        # sets the geometry of toplevel
        newWindow.geometry("700x700")
    
        # A Label widget to show in toplevel
        text= Text(newWindow,wrap=WORD, font=("Arial",25))
        content = self.listBox.item(curItem)
        content = content['values'] # show all contents about the selected film

        for elem in content:
            elem = str(elem)
            elem += '\n\n'

            text.insert(INSERT,elem)
        
        text.pack()

    def db_update(self):
        greeting_maker = Pyro4.Proxy("PYRONAME:example.greeting")
        greeting_maker.db_update()

    def dump_treeview(self):
        greeting_maker = Pyro4.Proxy("PYRONAME:example.greeting")
        # cursor = greeting_maker.db_dump()
        rows = greeting_maker.get_film()

        to_write = []
        for elem in rows:
                to_write.append(elem[0] + ', ' + elem[1] + ', ' +  elem[2] + ', ' +  elem[3] + ', ' +  elem[4] + ', ' +  elem[5] + ', ' +  elem[6] + ', ' +  elem[7] + '\n')

        with open('film_dump.txt', 'w') as file:
            for l in to_write:
                file.write(l)

        # old way to save it into csv, but it does not work. I cannot return a cursor from server when the db connection is closed. Basically
        # the cursor is unuseful
        # with open('output.csv','w') as out_csv_file:
        #     csv_out = csv.writer(out_csv_file)
        #     # write header                        
        #     # csv_out.writerow([d[0] for d in cursor])
        #     # write data                          
        #     csv_out.writerow(cursor)

    def register(self):
        greeting_maker = Pyro4.Proxy("PYRONAME:example.greeting")

        username = self.T1.get("1.0", "end")
        password_hashed = self.T2.get("1.0", "end")
        password_hashed = hashlib.sha256(password_hashed.encode('utf-8')).hexdigest()

        print("username: ", username)
        print("hash: ", password_hashed)

        greeting_maker.user_registration(username, password_hashed, str(self.favourites_list))    

    def login(self):
        greeting_maker = Pyro4.Proxy("PYRONAME:example.greeting")


        username = self.T1.get("1.0", "end")
        self.password_hashed = self.T2.get("1.0", "end")
        self.password_hashed = hashlib.sha256(self.password_hashed.encode('utf-8')).hexdigest()

        # print("username: ", username)
        # print("hash: ", self.password_hashed)

        res = greeting_maker.user_login(username, self.password_hashed, str(self.favourites_list))
        if res:
            print("utente loggato correttamente")
            self.login_label.config(text=username)
            
            self.l1.destroy()
            self.l2.destroy()
            self.T1.destroy()
            self.T2.destroy()
            self.RegisterButton.destroy()
            self.LoginButton.destroy()

            with open('logged_username.txt', 'w') as f:
                f.write(username)

        else:
            print("utente non loggato")

    def print_all_user(self):
        greeting_maker = Pyro4.Proxy("PYRONAME:example.greeting")

        greeting_maker.user_print_all()

    def add_favourites(self):
        curItem = self.listBox.focus()
        self.favourites_list.append(self.listBox.item(curItem))

    def update_favourites(self):       
        greeting_maker = Pyro4.Proxy("PYRONAME:example.greeting")
        greeting_maker.update_fav(self.login_label.cget('text'), str(self.favourites_list), self.password_hashed)

    def show_info_prices(self):
        greeting_maker = Pyro4.Proxy("PYRONAME:example.greeting")

        newWindow = tk.Tk()
        newWindow.title("Info")
        newWindow.geometry("700x700")
    

        text= Text(newWindow,wrap=WORD, font=("Arial",25))
        contentOdd, contentEven =  greeting_maker.get_info_price()
        
        for elem in contentOdd:
            text.insert(INSERT,elem + '\n')
        
        for elem in contentEven:
            text.insert(INSERT, elem + '\n')

        text.pack()

    def dump_favourites_list(self):
        greeting_maker = Pyro4.Proxy("PYRONAME:example.greeting")
        arg = self.login_label.cget('text')
        res = greeting_maker.dump_fav(arg)
        print("Risultati favoriti: ", res)
        with open('favourites_list.txt', 'w') as f:
            f.write(res)

    def film_chat(self):
        greeting_maker = Pyro4.Proxy("PYRONAME:example.greeting")
        self.chat_server_thread = greeting_maker.chat_server() # -> one day I have to handle this thing differently. Maybe I can do the same thing but sending a message to the server for closing the thread!!!
                                                              # but now is the exact day before the presentation, so I'm not gonna do anymore changes

        self.thread = threading.Thread(target= self.chat_client)
        self.thread.start()

    def chat_client(self):
        call(['python', 'chat_client.py'])

    def kill_threads(self):
        self.thread.stop()
        self.chat_server_thread
    

def main():
    root = Tk()
    app = tofu(root)
    root.mainloop()

if __name__ == '__main__':
    main()



