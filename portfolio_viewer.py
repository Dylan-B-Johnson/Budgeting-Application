import tkinter as tk
from tkinter import *
from tkinter_toolbox import Dlabel


window2=Tk()
window2.title("Finance Helper-Portfolio Viewer")
window2.geometry('1080x720')
#window2.option_add("*Font", "arial 12")

lbl = Label(window2,text="Add or remove stocks from your portfolio by typing the stock's ticker, followed by a space and the number of shares to be added/removed.\n"+
            'To enter multiple at once, simpily add a comma and one space between them.\n Example: "AMZN 4, AAPL 5"')
lbl.grid(column=1, row=1)
txt = Entry(window2,width=120)
txt.grid(column=1, row=2)
    
window2.mainloop()
