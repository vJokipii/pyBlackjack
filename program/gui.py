from tkinter import *
from tkinter import ttk

#Luodaan ikkuna
root = Tk()
root.title("Blackjack")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

#Funktioita
def calculate():
    root.title("Click")

#Luodaan käyttöliittymä
ttk.Button(mainframe, text="Button", command=calculate).grid(column=3, row=3, sticky=W)
root.geometry("500x500")

#Mainloop
root.mainloop()