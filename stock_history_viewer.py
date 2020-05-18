import tkinter 
import budgeting_app as ba
from tkinter_toolbox import bubble_options
from tkinter_toolbox import Denter
from tkinter_toolbox import Dlabel
from tkinter_toolbox import Dbox
import matplotlib.pyplot as plt
from yahoo_fin import stock_info as si
from tkinter import messagebox

def graph_history():
	ticker=stock_box.get()
	if tried:
		# try:
		x=si.get_data(ticker)
		new_indexes=[i for i in range(len(x.index))]
		if radio_values.get()==0:
			plt.plot(x.index,list(x['adjclose']))
			plt.title(ticker.upper()+' Closing Price History')
			plt.ylabel(ticker.upper()+' Closing Value in USD')
			plt.xlabel('Time Since '+ticker.upper()+' Went Public')
		if radio_values.get()==1: time=365
		if radio_values.get()==2: time=31
		if radio_values.get()==3: time=7
		if radio_values.get()==4: time=91
		if radio_values.get()!=0:
			plt.plot(x.index[-time:],list(x['adjclose'])[-time:])
			plt.title(ticker.upper()+' Closing Price History')
			plt.ylabel(ticker.upper()+' Closing Value in USD')
			plt.xlabel('Past '+str(time)+' Days')
		plt.show()
		# # except: 
		# 	messagebox.showinfo('Ticker Invalid','It appears that \''+ticker.upper()+'\' is not a valid stock ticker. '+
		# 			'As such its history cannot be graphed. Please check for typos or try searching for the company\'s ticker.')

def open_viewer(prev_window):
	global tried
	global radio_values
	global rad_list
	tried=False
	global stock_box
	window3=tkinter.Toplevel(prev_window)
	window3.title("Finance Helper-Single Stock History Viewer")
	window3.geometry('760x120')
	window3.option_add("*Font", "arial 12")
	radio_values=tkinter.IntVar()
	bubble_options(radio_values,window3,3,0,5,['All Time','One Year','One Quarter','One Month','One Week'], lambda: print(radio_values.get()))
	stock_box=Dbox(window3,'Stock Ticker:',0,0)
	graph_button=tkinter.Button(window3,text='Graph',command=lambda: graph_history())
	graph_button.grid(column=2, row=0)
	tried=True
	window3.mainloop()