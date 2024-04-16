from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


'''
gets the latest messages from the server and inserts it into the Listbox object.
If the window has somehow been closed abruptly, we remove the user.
'''
def receive():
    stop = False
    while True and not stop:
        try:
            msg = clientSocket.recv(BUFFSIZE).decode('utf8')
            msgList.insert(tkinter.END,msg)
        except OSError:
            cleanAndClose()
            break

'''
it function sends the messages of the user to the server to be broadcast, 
if the exit sequence is entered, user's data is purged, and the window is closed.
'''
def send(event=None):
    msg = myMsg.get()
    myMsg.set("")
    clientSocket.send(bytes(msg,'utf8'))
    if msg == "'exit'":
        clientSocket.close()
        cleanAndClose()
        # top.quit()
        top.destroy()


def cleanAndClose(event=None):
    # this trick was not working properly
    # myMsg.set("exit")
    # send()
    top.destroy()
    # stop = True

if __name__ == '__main__':
    top = tkinter.Tk()
    top.title('ChatRoom')
    messageFrame = tkinter.Frame(top)
    scrollbar = tkinter.Scrollbar(messageFrame)

    msgList = tkinter.Listbox(messageFrame, width = 50, yscrollcommand = scrollbar.set)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    msgList.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    msgList.pack(fill = tkinter.X)
    messageFrame.pack()

    myMsg = tkinter.StringVar()

    username = 'user'

    try:
        with open('logged_username.txt', 'r') as f:
            username = f.read()

        username = username.replace('\n','')
        print('Utente loggato come: ', username)
    except:
        print('Nessun utente loggato')

    myMsg.set(username)
    entryField = tkinter.Entry(top,textvariable = myMsg)
    entryField.bind("<Return>", send)
    entryField.pack()
    sendButton = tkinter.Button(top, text = 'Send', command = send, height = 1, width = 7)
    sendButton.pack()

    top.protocol("WM_DELETE_WINDOW", cleanAndClose)

    # removing stuff that I need to take from user input stdin
    # HOST = input('Enter HOST IP Address: ')
    # PORT = input('Enter PORT number: ')
    # PORT = 5545 if not PORT else int(PORT)

    # default port, not to use in production
    HOST = '127.0.0.1'
    PORT = 5545

    BUFFSIZE = 1024
    ADDR = (HOST, PORT)
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(ADDR)

    receiveThread = Thread(target=receive)
    receiveThread.start()
    tkinter.mainloop()  
    receiveThread.join()