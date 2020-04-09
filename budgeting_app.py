print('Loading...\nThis will take a suprisingly long amount of time.')
import tkinter as tk
from tkinter import *
import tkinter_toolbox as t
from tkinter_toolbox import Dlabel
from tkinter_toolbox import Denter
from tkinter import messagebox
from tkinter_toolbox import bouble_options
from tkinter_toolbox import Denter2


def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

def enter_pressed():
    if income_box.get().isnumeric()==False: messagebox.showinfo('Number Error', 'You must enter a number in the income box')
    else:
        global current_gross
        current_gross=income_box.get()
        current_income.configure(text=('$'+income_box.get()))
        build_3rd_row()

def boubles():
    if bouble_var.get()==0: income.configure(text='Annual Gross Income:')
    if bouble_var.get()==1: income.configure(text='Monthly Gross Income:')
    if bouble_var.get()==2: income.configure(text='Weekly Gross Income:')

def build_3rd_row():
    #builds 3rd row (income taxes)
    global lbl_3rd
    global box_3rd
    global lbl_3rd_2
    global enter_3rd
    global box_3rd_2
    lbl_3rd=Dlabel(window,'Percent Income Tax:',0,2)
    box_3rd=Entry(window,width=10)
    box_3rd.grid(column=1, row=2)
    lbl_3rd_2=Dlabel(window,'Any Additional Flat Income Taxes:',2,2)
    box_3rd_2=Entry(window,width=10)
    box_3rd_2.grid(column=3, row=2)
    enter_3rd = Button(window,text='Enter', command=lambda:save_tax())
    enter_3rd.grid(column=4, row=2)

#returns the annual gross income as a STR
def get_annual():
    if bouble_var.get()==0:
        return current_gross
    if bouble_var.get()==1:
        x=str(float(current_gross)*12.0)
        return x
    if bouble_var.get()==2:
        x=str(float(current_gross)*52.1429)
        return x

#returns the net income in a given time frame as a FLOAT
def get_net(time):
    if time=='weekly':
        x=float(net)/52.1429
        return x
    if time=='monthly':
        x=float(net)/12.0
        return x
    if time=='yearly':
        x = float(net)
        return x

def build_output_innputs():
    #builds budget output
    global output_inputs
    global output_labels
    global output_boubles
    output_labels=[]
    output_inputs=[]
    output_boubles=[IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar()]
    i2=0
    for i in ['Housing:','Utilities:','Food:','Transportation:','Clothing:','Medical:','Discretionary:','Savings:']:
        output_inputs.append(Denter2(window,i,0,(i2+5),output_buttons,i))
        output_labels.append(Dlabel(window,(i+' $'+truncate((get_net('weekly')*get_default_percent(i)),2)+' per week, $'+
                       truncate((get_net('monthly')*get_default_percent(i)),2)+' per month, and $'+
                       truncate((get_net('yearly')*get_default_percent(i)),2)+' per year'),3,(6+i2)))
        t.bouble_options(output_boubles[i2],window,4,(i2+5),2,['Percent','Dollars'],bouble_effect())
        i2+=1

def bouble_effect():
    #change from percent to dollars or visa versa
    pass

def save_tax():
    if box_3rd.get().isnumeric()== False or box_3rd_2.get().isnumeric()==False: messagebox.showinfo('Number Error', 'You must enter a number in the tax box')
    else:
        global net
        net=str(float(get_annual())*(1-int(box_3rd.get())/100)-(int(box_3rd_2.get())))
        net_income=Dlabel(window,('Net Income: $'+truncate(net,2)+' per year,\n$'+
           str(truncate(((float(net))/12.0),2))+' per month,\n$'+
           str(truncate(((float(net))/52.1429),2))+' per week'),0,4)
        build_output_innputs()
        
def get_default_percent(category):
    if category=='Housing:': return .35
    if category=='Utilities:': return .05
    if category=='Food:': return .14
    if category=='Transportation:': return .15
    if category=='Clothing:': return .03
    if category=='Medical:': return .03
    if category=='Discretionary:': return .05
    if category=='Savings:': return .2
    
#TKTKTKTKTKTKTKTKTKT Will hold the 
def output_buttons(category):
    i2=0
    for i in ['Housing:','Utilities:','Food:','Transportation:','Clothing:','Medical:','Discretionary:','Savings:']:
        print(output_inputs[i2].get())
        i2+=1
             

#only runs if the file is running (so that functions ^ can be used)
# Doesn't work now, since you have print('Loading') at the top
if __name__ == "__main__":
    window=Tk()
    window.title("Finance Helper-This is for budget exploration; it should not replace the help of a financial professional.-Dylan J.")
    window.geometry('720x480')
    
    #builds 1st two rows
    income=Label(window, text="Annual Gross Income:")
    income_box= Entry(window,width=10)
    current_income=Label(window,text='')
    enter = Button(window,text='Enter', command=lambda: enter_pressed())

    #places 1st two rows
    income.grid(column=0, row=0)
    income_box.grid(column=1, row=0)
    enter.grid(column=2, row=0)
    current_income.grid(column=0,row=1)

    #sets bouble options in 1st row
    bouble_var=IntVar()
    t.bouble_options(bouble_var,window,4,0,3,['Annually','Monthly','Weekly'],boubles)

    window.mainloop()
