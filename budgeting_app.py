import tkinter as tk
from tkinter import *
import matplotlib.pyplot as plt
import matplotlib as mpl
import tkinter_toolbox as t
from tkinter_toolbox import Dlabel
from tkinter_toolbox import Denter
from tkinter import messagebox
from tkinter_toolbox import bouble_options
from tkinter_toolbox import Denter2
from tkinter_toolbox import Denter3
import pickle
global budget_num
global last_budget
global shell
global shell2
global user_location
user_location=0
shell=''
shell2=''
last_budget=[]
budget_num=0
mpl.rcParams['font.size'] = 7.0 #changes matplot lib fornt size

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

def enter_pressed(num):
    global user_location
    user_location=1
    if (income_box.get().isnumeric()==False) and num==1: messagebox.showinfo('Number Error', 'You must enter a number in the income box')
    else:
            global current_gross
            if num==1: current_gross=income_box.get()
            if num==2:current_gross=float(truncate(net,2))
            if (num==1): current_income.configure(text=('$'+income_box.get()))
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
    enter_3rd = Button(window,text='Enter', command=lambda:save_tax(1))
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
    #builds budget output or default budget 
    global output_inputs
    global output_inputs_og
    global output_labels
    global output_boubles
    global budget_num
    global last_budget
    global shell
    global shell2
    global user_location
    user_location=3
    output_labels=[]
    last_budget=[]
    output_inputs_og=[]
    output_boubles=[IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar()]
    i2=0
    for i in ['Housing:','Utilities:','Food:','Transportation:','Clothing:','Medical:','Discretionary:','Savings:']:
        output_inputs_og.append(Denter3(window,i,0,(i2+5)))
        output_labels.append(Dlabel(window,(' $'+truncate((get_net('weekly')*get_default_percent(i)),2)+'/wk    $'+
                       truncate((get_net('monthly')*get_default_percent(i)),2)+'/mo    $'+
                       truncate((get_net('yearly')*get_default_percent(i)),2)+'/yr'),2,(5+i2)))
        last_budget.append(float(truncate((get_net('yearly')*get_default_percent(i)),2)))
        t.bouble_options(output_boubles[i2],window,3,(i2+5),4,['Percent','Dollars (Weekly)','Dollars (Monthly)','Dollars (Yearly)'],bouble_effect(i2))
        i2+=1
        
    if budget_num==0: #printing reccomended budget
        print('\n----------------------------------DEFAULT BUDGET--------------------------------')
        shell+='\nDEFAULT BUDGET\n'
        shell2+='\n----------------------------------DEFAULT BUDGET--------------------------------\n'
        for i in ['Housing:','Utilities:','Food:','Transportation:','Clothing:','Medical:','Discretionary:','Savings:']:
            if (i=='Food:'):
                print(i+'\t\t$'+truncate((get_net('weekly')*get_default_percent(i)),2)+'/wk\t$'+
                       truncate((get_net('monthly')*get_default_percent(i)),2)+'/mo\t$'+
                       truncate((get_net('yearly')*get_default_percent(i)),2)+'/yr')
                temp=(i+'\t\t$'+truncate((get_net('weekly')*get_default_percent(i)),2)+'/wk\t$'+
                       truncate((get_net('monthly')*get_default_percent(i)),2)+'/mo\t$'+
                       truncate((get_net('yearly')*get_default_percent(i)),2)+'/yr\n')
                shell+=temp
                shell2+=temp
            else:
                print(i+'\t$'+truncate((get_net('weekly')*get_default_percent(i)),2)+'/wk\t$'+
                       truncate((get_net('monthly')*get_default_percent(i)),2)+'/mo\t$'+
                       truncate((get_net('yearly')*get_default_percent(i)),2)+'/yr')
                temp=(i+'\t$'+truncate((get_net('weekly')*get_default_percent(i)),2)+'/wk\t$'+
                       truncate((get_net('monthly')*get_default_percent(i)),2)+'/mo\t$'+
                       truncate((get_net('yearly')*get_default_percent(i)),2)+'/yr\n')
                shell+=temp
                shell2+=temp
        budget_num+=1
        
    enter = Button(window,text='Calculate Budget', command=lambda: output_buttons())
    enter.grid(column=1, row=14)
    enter = Button(window,text='Reset Budget to Default', command=lambda: build_output_innputs())
    enter.grid(column=2, row=14)
    enter = Button(window,text='Generate Pie Chart', command=lambda: build_budget_piechart())
    enter.grid(column=3, row=14)
    enter = Button(window,text='Export Budgets to Word', command=lambda: save_shell('word'))
    enter.grid(column=4, row=14)
    enter = Button(window,text='Export Budgets to Text', command=lambda: save_shell('text'))
    enter.grid(column=5, row=14)

def save_shell(file_type):
    global shell
    global shell2
    if file_type=='word':
        file = open('budget.docx','w')
        file.write(shell)
    else:
        file = open('budget.txt','w')
        file.write(shell2)
    file.close()
    
def bouble_effect(bouble_row_num):
    #percent to dollars button press
    pass

def save_tax(num):
    global user_location
    user_location=2
    if (box_3rd.get().isnumeric()== False or box_3rd_2.get().isnumeric()==False) and (num==1): messagebox.showinfo('Number Error', 'You must enter a number in the tax box')
    else:
        global net
        if num==1: net=str(float(get_annual())*(1-int(box_3rd.get())/100)-(int(box_3rd_2.get())))
        net_income=Dlabel(window,('Net Income: $'+truncate(net,2)+' per year,\n$'+
           str(truncate(((float(net))/12.0),2))+' per month,\n$'+
           str(truncate(((float(net))/52.1429),2))+' per week'),0,4)
        if num==1 or num==3: build_output_innputs()
        
def get_default_percent(category):
    if category=='Housing:': return .35
    if category=='Utilities:': return .05
    if category=='Food:': return .14
    if category=='Transportation:': return .15
    if category=='Clothing:': return .03
    if category=='Medical:': return .03
    if category=='Discretionary:': return .05
    if category=='Savings:': return .2

# updates the budget based on what the user entered
def update_budget():
        global budget_num
        global last_budget
        global shell
        global shell2
        output_labels=[]
        last_budget=[]
        i2=0
        print('\n------------------------------------BUDGET #'+str(budget_num)+'-----------------------------------')
        shell=(shell+'\nBUDGET #'+str(budget_num)+'\n')
        shell2+='\n------------------------------------BUDGET #'+str(budget_num)+'-----------------------------------\n'
        budget_num+=1
        for i in ['Housing:','Utilities:','Food:','Transportation:','Clothing:','Medical:','Discretionary:','Savings:']:
             if i2 in blank_list:
                 last_budget.append(float(truncate((new_blank_dollars[0]),2)))
                 output_labels.append(Dlabel(window,(' $'+truncate((new_blank_dollars[0]/52.1429),2)+'/wk    $'+
                       truncate((new_blank_dollars[0]/12),2)+'/mo    $'+
                       truncate((new_blank_dollars[0]),2)+'/yr'),2,(5+i2)))
                 if (i=='Food:'):
                             temp=(i+'\t\t$'+truncate((new_blank_dollars[0]/52.1429),2)+'/wk\t$'+   #these prints really should have been a function
                                           truncate((new_blank_dollars[0]/12),2)+'/mo\t$'+
                                           truncate((new_blank_dollars[0]),2)+'/yr\n')
                             shell+=temp
                             shell2+=temp
                             print(i+'\t\t$'+truncate((new_blank_dollars[0]/52.1429),2)+'/wk\t$'+
                                           truncate((new_blank_dollars[0]/12),2)+'/mo\t$'+
                                           truncate((new_blank_dollars[0]),2)+'/yr')
                 else:
                     temp=(i+'\t$'+truncate((new_blank_dollars[0]/52.1429),2)+'/wk\t$'+
                                       truncate((new_blank_dollars[0]/12),2)+'/mo\t$'+
                                       truncate((new_blank_dollars[0]),2)+'/yr\n')
                     shell+=temp
                     shell2+=temp
                     print(i+'\t$'+truncate((new_blank_dollars[0]/52.1429),2)+'/wk\t$'+
                                       truncate((new_blank_dollars[0]/12),2)+'/mo\t$'+
                                       truncate((new_blank_dollars[0]),2)+'/yr')
                 del new_blank_dollars[0]
             if i2 in dollar_list:
                 last_budget.append(float(truncate((dollar_ammount_annual[0]),2)))
                 output_labels.append(Dlabel(window,(' $'+truncate((dollar_ammount_annual[0]/52.1429),2)+'/wk    $'+
                       truncate((dollar_ammount_annual[0]/12),2)+'/mo    $'+
                       truncate((dollar_ammount_annual[0]),2)+'/yr'),2,(5+i2)))
                 if (i=='Food:'):
                     temp=(i+'\t\t$'+truncate((dollar_ammount_annual[0]/52.1429),2)+'/wk\t$'+
                                       truncate((dollar_ammount_annual[0]/12),2)+'/mo\t$'+
                                       truncate((dollar_ammount_annual[0]),2)+'/yr\n')
                     shell+=temp
                     shell2+=temp
                     print(i+'\t\t$'+truncate((dollar_ammount_annual[0]/52.1429),2)+'/wk\t$'+
                                       truncate((dollar_ammount_annual[0]/12),2)+'/mo\t$'+
                                       truncate((dollar_ammount_annual[0]),2)+'/yr')
                 else:
                     temp=(i+'\t$'+truncate((dollar_ammount_annual[0]/52.1429),2)+'/wk\t$'+
                                       truncate((dollar_ammount_annual[0]/12),2)+'/mo\t$'+
                                       truncate((dollar_ammount_annual[0]),2)+'/yr\n')
                     shell+=temp
                     shell2+=temp
                     print(i+'\t$'+truncate((dollar_ammount_annual[0]/52.1429),2)+'/wk\t$'+
                                       truncate((dollar_ammount_annual[0]/12),2)+'/mo\t$'+
                                       truncate((dollar_ammount_annual[0]),2)+'/yr')
                 del dollar_ammount_annual[0]
             if i2 in percent_list:
                 last_budget.append(float(truncate((percent_dollars[0]),2)))
                 output_labels.append(Dlabel(window,(' $'+truncate((percent_dollars[0]/52.1429),2)+'/wk    $'+
                       truncate((percent_dollars[0]/12),2)+'/mo    $'+
                       truncate((percent_dollars[0]),2)+'/yr'),2,(5+i2)))
                 if (i=='Food:'):
                     temp=(i+'\t\t$'+truncate((percent_dollars[0]/52.1429),2)+'/wk\t$'+
                                       truncate((percent_dollars[0]/12),2)+'/mo\t$'+
                                       truncate((percent_dollars[0]),2)+'/yr\n')
                     shell+=temp
                     shell2+=temp
                     print(i+'\t\t$'+truncate((percent_dollars[0]/52.1429),2)+'/wk\t$'+
                                       truncate((percent_dollars[0]/12),2)+'/mo\t$'+
                                       truncate((percent_dollars[0]),2)+'/yr')
                 else:
                     temp=(i+'\t$'+truncate((percent_dollars[0]/52.1429),2)+'/wk\t$'+
                                       truncate((percent_dollars[0]/12),2)+'/mo\t$'+
                                       truncate((percent_dollars[0]),2)+'/yr\n')
                     shell+=temp
                     shell2+=temp
                     print(i+'\t$'+truncate((percent_dollars[0]/52.1429),2)+'/wk\t$'+
                                       truncate((percent_dollars[0]/12),2)+'/mo\t$'+
                                       truncate((percent_dollars[0]),2)+'/yr')
                 del percent_dollars[0]
             i2+=1
   
#Activated when budget changing buttons are enttered 
def output_buttons():
    global blank_list
    global dollar_list
    global dollar_ammount_sum
    global percent_list
    global percent_dollars
    global default_budget
    global dollar_ammount_annual
    dollar_ammount_sum_annual=0
    dollar_ammount_annual=[]
    dollar_list=[]
    output_inputs=[]
    for i in range(8):
       if output_inputs_og[i].get().isnumeric()==True: output_inputs.append(int(output_inputs_og[i].get()))
       else: output_inputs.append(output_inputs_og[i].get())
    

    #---------------------------------------Finding the indecies of each category of bouble option--------------------------------------------------
    blank_list=[i for i in range(8) if output_inputs_og[i].get().isnumeric()==False]
    percent_list=[i for i in range(8) if (output_boubles[i].get()==0) and (output_inputs_og[i].get().isnumeric()==True)]
    for i in range(8):
        if (output_boubles[i].get() in [1,2,3]) and (output_inputs_og[i].get().isnumeric()==True):
            dollar_list.append(i)
        if (output_boubles[i].get()==1) and (output_inputs_og[i].get().isnumeric()==True):
            dollar_ammount_sum_annual+=(output_inputs[i]*52.1429)
            dollar_ammount_annual.append(output_inputs[i]*52.1429)
        if (output_boubles[i].get()==2) and (output_inputs_og[i].get().isnumeric()==True):
            dollar_ammount_sum_annual+=(output_inputs[i]*12)
            dollar_ammount_annual.append(output_inputs[i]*12)
        if (output_boubles[i].get()==3) and (output_inputs_og[i].get().isnumeric()==True):
            dollar_ammount_sum_annual+=(output_inputs[i])
            dollar_ammount_annual.append(output_inputs[i]) 

    #---------------------------------------------------Error Handeling-----------------------------------------------------------------------------
    error_had=False
    if (len(blank_list)+len(dollar_list)+len(percent_list))!=8:
        messagebox.showinfo('Budget Error', 'Something went wrong. Make sure that there are no nonnumerics in the budget input boxes (unfortunately '+
                            'decimals are not supported). Also make sure that you have selected the type of number you are inputing with the boubles on the right'+
                            ' (e.g. percent or dollars).')
        error_had=True
        
    temp_percent_sum=0
    for i in percent_list: temp_percent_sum+=output_inputs[i]
    
    if temp_percent_sum > 100:
        error_had=True
        messagebox.showinfo(('Percent Error: '+str((temp_percent_sum-100))+'% Over'),'The percentages you entered in your budget are greater than 100% by '+str((temp_percent_sum-100))+
                            ' percent. Check for typos, or try cutting back somewhere.')
        
    if (dollar_ammount_sum_annual>float(net)):
        error_had=True
        messagebox.showinfo(('Expenditure Error: $'+truncate((dollar_ammount_sum_annual-float(net)),2)+' Over'),'The expenses you have entered into your budget exceed your net income by $'+truncate((dollar_ammount_sum_annual-float(net)),2)+
                            ' Check for typos, or try cutting back somewhere.')
        
    if (dollar_ammount_sum_annual==float(net) and temp_percent_sum>0):
        error_had=True
        messagebox.showinfo('Budget Error','The expenses you have entered into your budget are equal to your net income.'+
                            ' You therefore cannot allocate any additional funds as a percentage. Check for typos, or try cutting back somewhere.')

    #------------------------------------------------------------Processing-------------------------------------------------------------------------
    expense_net = float(net) - dollar_ammount_sum_annual
    percent_dollars = [(expense_net*(output_inputs[i])/100) for i in percent_list]
    pre_blank_net = expense_net-sum(percent_dollars)

    default_budget=[.35,.05,.14,.15,.03,.03,.05,.2]
    default_budget_blank_sum=0
    for i in blank_list:
        default_budget_blank_sum+=default_budget[i]
        
    global new_blank_dollars
    new_blank_dollars=[(pre_blank_net*default_budget[i]/default_budget_blank_sum) for i in blank_list]
    if error_had==False: update_budget()

def build_budget_piechart():
    global last_budget
    labels='Housing','Utilities','Food','Transportation','Clothing','Medical','Discretionary','Savings'
    fig1, ax1 = plt.subplots()
    ax1.pie(last_budget, labels=labels, autopct='%1.1f%%',
        shadow=False)
    ax1.axis('equal')
    plt.show()

#saves budget for loading later
def save_budget():
    global budget_num
    global last_budget
    if budget_num<1: messagebox.showinfo('Error: No Budget to Save','You have not created a budget to be saved yet. Fill in the income and tax boxes to generate a default budget.'+
                                         ' You can then create your own personalized budget to save.')
    else:
        file = open('last_budget','wb')
        pickle.dump(last_budget,file)
        f = open('last_income','w')
        f.write(net)
        f.close()
        file.close()
        
def load_budget():
    global net
    global last_budget
    global shell
    global shell2
    global output_labels
    global budget_num
    global user_location
        
    output_labels=[]
    f_budget=open('last_budget','rb')
    f_income=open('last_income','r')
    net=f_income.readline()
    last_budget=pickle.load(f_budget)
    if user_location<1:
        enter_pressed(2)
    if user_location<2:
        save_tax(3)
    if user_location <3:
        build_output_innputs()
    save_tax(2)
    i2=0
    print('\n-------------------------------BUDGET #'+str(budget_num)+' (LOADED)-------------------------------')
    shell=(shell+'\nBUDGET #'+str(budget_num)+' (LOADED)\n')
    shell2+='\n-------------------------------BUDGET #'+str(budget_num)+' (LOADED)-------------------------------\n'
    budget_num+=1
    for i in ['Housing:','Utilities:','Food:','Transportation:','Clothing:','Medical:','Discretionary:','Savings:']:
                 output_labels.append(Dlabel(window,(' $'+truncate((last_budget[i2]/52.1429),2)+'/wk    $'+
                       truncate((last_budget[i2]/12),2)+'/mo    $'+
                       truncate((last_budget[i2]),2)+'/yr'),2,(5+i2)))
                 if (i=='Food:'):
                             temp=(i+'\t\t$'+truncate((last_budget[i2]/52.1429),2)+'/wk\t$'+   #these prints really should have been a function
                                           truncate((last_budget[i2]/12),2)+'/mo\t$'+
                                           truncate((last_budget[i2]),2)+'/yr\n')
                             shell+=temp
                             shell2+=temp
                             print(i+'\t\t$'+truncate((last_budget[i2]/52.1429),2)+'/wk\t$'+
                                           truncate((last_budget[i2]/12),2)+'/mo\t$'+
                                           truncate((last_budget[i2]),2)+'/yr')
                 else:
                     temp=(i+'\t$'+truncate((last_budget[i2]/52.1429),2)+'/wk\t$'+
                                       truncate((last_budget[i2]/12),2)+'/mo\t$'+
                                       truncate((last_budget[i2]),2)+'/yr\n')
                     shell+=temp
                     shell2+=temp
                     print(i+'\t$'+truncate((last_budget[i2]/52.1429),2)+'/wk\t$'+
                                       truncate((last_budget[i2]/12),2)+'/mo\t$'+
                                       truncate((last_budget[i2]),2)+'/yr')
                 i2+=1

#only runs if the file is running (so that functions ^ can be used)
# Doesn't work now, since you have print('Loading') at the top
if __name__ == "__main__":
    window=Tk()
    window.title("Finance Helper-This is for budget exploration; it should not replace the help of a financial professional.-Dylan J.")
    window.geometry('1080x720')

    #builds menu bars
    menu = Menu(window)
    new_item = Menu(menu)
    new_item.add_command(label='Save Budget and Income',command=lambda: save_budget())
    new_item.add_command(label='Load Budget and Income',command=lambda: load_budget())
    menu.add_cascade(label='File', menu=new_item)
    window.config(menu=menu)
    
    #builds 1st two rows
    income=Label(window, text="Annual Gross Income:")
    income_box= Entry(window,width=10)
    current_income=Label(window,text='')
    enter = Button(window,text='Enter', command=lambda: enter_pressed(1))

    #places 1st two rows
    income.grid(column=0, row=0)
    income_box.grid(column=1, row=0)
    enter.grid(column=2, row=0)
    current_income.grid(column=0,row=1)

    #sets bouble options in 1st row
    bouble_var=IntVar()
    t.bouble_options(bouble_var,window,4,0,3,['Annually','Monthly','Weekly'],boubles)

    window.mainloop()
