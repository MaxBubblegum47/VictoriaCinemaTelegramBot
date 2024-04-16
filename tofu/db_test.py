import sqlite3

connection = sqlite3.connect("movies.db")

cursor = connection.cursor()
cursor.execute("SELECT * FROM example")
rows = cursor.fetchall()

# Print elements actually in the database


connection.close()

from tkinter import *
  
# Create object 
root = Tk() 
  
# Adjust size 
root.geometry( "200x200" ) 
  
# Change the label text 
def day_it(day):
    if day == 'Monday':
        day = 'Lunedì'
        return day
    
    if day == 'Tuesday':
        day == 'Martedì'
        return day
    
    if day == 'Wednesday':
        day == 'Mercoledì'
        return day
    
    if day == 'Thursday':
        day == 'Giovedì'
        return day
    
    if day == 'Friday':
        day == 'Venerdì'
        return day
    
    if day == 'Saturday':
        day == 'Sabato'
        return day
    
    if day == 'Sunday':
        day == 'Domenica'
        return day
    


def choose_day(): 
    label.config( text = clicked.get() ) 
    day = label.cget('text')
    day = day_it(day)

    print(day)


    for row in rows:
        s  = ''.join(row)
    if day in s:
        print(s)

  
# Dropdown menu options 
options = [ 
    "Monday", 
    "Tuesday", 
    "Wednesday", 
    "Thursday", 
    "Friday", 
    "Saturday", 
    "Sunday"
] 
  
# datatype of menu text 
clicked = StringVar() 
  
# initial menu text 
clicked.set( "Monday" ) 
  
# Create Dropdown menu 
drop = OptionMenu( root , clicked , *options ) 
drop.pack() 
  
# Create button, it will change label text 
button = Button( root , text = "click Me" , command = choose_day).pack() 
  
# Create Label 
label = Label( root , text = " " ) 
label.pack() 


# Execute tkinter 
root.mainloop() 