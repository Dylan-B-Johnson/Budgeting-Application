# A module for easy GUI creation

from tkinter import Radiobutton
from tkinter import Label
from tkinter import Entry
from tkinter import Button 

#a function which easily creates a number of bubble radio buttons
def bubble_options(var,tkinter,column_start,row,option_num,option_labels,option_effect):
    rad_list=[]
    for i in range(option_num):
        rad=Radiobutton(tkinter,text=(option_labels[i]),variable=var,value=i,command=option_effect)
        rad_list.append(rad)
    i2=0
    for rad in rad_list:
        rad.grid(column=(column_start+i2),row=row)
        i2+=1

# a class that displays a text box
class Dlabel:
    def __init__(self,tkinter,text1,column1,row1):
        lbl=Label(tkinter, text=text1)
        lbl.grid(column=column1,row=row1)
        self.text=text1
        self.column=column1
        self.row=row1
    def configure(self,text2):
        self.text=text2
        lbl.configure(text=text2)

# a class that creates a label, enter text box, and an enter button (in that order)
# on one row
class Denter:
    def __init__(self,tkinter,text,str_column,row,function):
        lbl=Dlabel(tkinter,text,str_column,row)
        box=Entry(tkinter,width=10)
        box.grid(column=(str_column+1), row=row)
        enter = Button(tkinter,text='Enter', command=function)
        enter.grid(column=(str_column+2), row=row)
        self.box=box
    def configure(self,text2):
        self.text=text2
        lbl.configure(text=text2)
    def get(self):
        self.value=self.box.get()
        return self.value

# Same as Denter, but with inputs for the command function
class Denter2:
    def __init__(self,tkinter,text,str_column,row,function,arg):
        lbl=Dlabel(tkinter,text,str_column,row)
        box=Entry(tkinter,width=10)
        box.grid(column=(str_column+1), row=row)
        enter = Button(tkinter,text='Enter', command=lambda: function(arg))
        enter.grid(column=(str_column+2), row=row)
        self.box=box
    def configure(self,text2):
        self.text=text2
        lbl.configure(text=text2)
    def get(self):
        self.value=self.box.get()
        return self.value

#same as first two Denters, but without an enter button 
class Denter3:
    def __init__(self,tkinter,text,str_column,row):
        lbl=Dlabel(tkinter,text,str_column,row)
        box=Entry(tkinter,width=10)
        box.grid(column=(str_column+1), row=row)
        self.box=box
    def configure(self,text2):
        self.text=text2
        lbl.configure(text=text2)
    def get(self):
        self.value=self.box.get()
        return self.value


        
    
