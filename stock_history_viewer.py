import tkinter as tk
import budgeting_app as ba
from tkinter_toolbox import bubble_options
from tkinter_toolbox import Denter
from tkinter_toolbox import Dlabel
from tkinter_toolbox import Dbutton
from tkinter_toolbox import Dbox
import matplotlib.pyplot as plt
from yahoo_fin import stock_info as si
from tkinter import messagebox
import pickle
import numpy as np

def graph_history(mode):
	if radio_values.get()==1: time=365
	if radio_values.get()==2: time=91
	if radio_values.get()==3: time=31
	if radio_values.get()==4: time=7
	if tried and mode=='single':
		ticker=stock_box.get()
		try:
			x=si.get_data(ticker)
			if radio_values.get()==0:
				plt.plot(x.index,list(x['adjclose']))
				plt.title(ticker.upper()+' Closing Price History')
				plt.ylabel(ticker.upper()+' Closing Value in USD')
				plt.xlabel('Time Since '+ticker.upper()+' Went Public')
			if radio_values.get()!=0:
				plt.plot(x.index[-time:],list(x['adjclose'])[-time:])
				plt.title(ticker.upper()+' Closing Price History')
				plt.ylabel(ticker.upper()+' Closing Value in USD')
				plt.xlabel('Past '+str(time)+' Days')
			plt.show()
		except: 
			messagebox.showinfo('Ticker Invalid','It appears that \''+ticker.upper()+'\' is not a valid stock ticker. '+
					'As such its history cannot be graphed. Please check for typos or try searching for the company\'s ticker.')
	if tried and (mode=='whole' or mode=='whole_no_tot'):
		try:
			stock_indexes=[]
			x=[]
			for i in range(len(stocks)):
				x.append(si.get_data(stocks[i][0]))
				if radio_values.get()==0:
					plt.plot(x[i].index,list(x[i]['adjclose']),label='Closing Value of '+str(stocks[i][0].upper()))
				else:
					plt.plot(x[i].index[-time:],list(x[i]['adjclose'])[-time:],label='Closing Value of '+str(stocks[i][0].upper()))
				stock_indexes.append(len(x[i].index))
			if mode!='whole_no_tot':
				oldest_stock_index=stock_indexes.index(max(stock_indexes))
				total_dollar_list=[]
				total_dollar_list=np.array(total_dollar_list)
				for date in x[oldest_stock_index].index:
					day_total=0
					for i in range(len(stocks)):
						if date in x[i].index:
							day_total+=x[i].at[date,'adjclose']*stocks[i][1]
					total_dollar_list=np.append(total_dollar_list,day_total)
				if radio_values.get()==0:
					plt.plot(x[oldest_stock_index].index,total_dollar_list,label='Total Value of Portfolio (Including Quantity of Stocks Presently Owned)')
					plt.xlabel('Time Since '+stocks[oldest_stock_index][0].upper()+' Went Public')
				if radio_values.get()!=0:
					plt.plot(x[oldest_stock_index].index[-time:],total_dollar_list[-time:],label='Total Value of Portfolio (Including Quantity of Stocks Presently Owned)')
					plt.xlabel('Past '+str(time)+' Days')
			plt.title('Portfolio Closing Price and Total Value History')
			plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), shadow=False, ncol=2)
			plt.ylabel('Closing Value in USD')
			plt.show()
		except:
			messagebox.showinfo('Error','Make sure that you have loaded a portfolio (under the file menu). If you do not have a portfolio to load, open the portfolio viewer under "tools" in the main budgeting app.'+
					' Also make sure that you are connected to the internet. If you have made a portfolio, make sure that the "portfolio" file is in the same directory as this application.')


def load_portfolio():
	global stocks
	f_port=open('portfolio','rb')
	stocks=pickle.load(f_port)


def open_viewer(prev_window):
	global tried
	global radio_values
	global rad_list
	tried=False
	global stock_box
	window3=tk.Toplevel(prev_window)
	window3.title("Finance Helper-Stock History Viewer")
	window3.geometry('785x120')
	window3.option_add("*Font", "arial 12")
	menu = tk.Menu(window3)
	new_item = tk.Menu(menu)
	new_item.add_command(label='Load Portfolio',command=lambda: load_portfolio())
	menu.add_cascade(label='File', menu=new_item)
	window3.config(menu=menu)
	radio_values=tk.IntVar()
	bubble_options(radio_values,window3,3,0,5,['All Time','One Year','One Quarter','One Month','One Week'], lambda: ba.bubble_effect())
	stock_box=Dbox(window3,'Stock Ticker:',0,0)
	graph_button=tk.Button(window3,text='Graph',command=lambda: graph_history('single'))
	graph_button.grid(column=2, row=0)
	graph_all_stocks=Dbutton(window3,'Graph Portfolio',lambda: graph_history('whole'),0,1)
	graph_all_stocks_no_tot=Dbutton(window3,'Graph Portfolio Without Total',lambda: graph_history('whole_no_tot'),0,2)
	tried=True
	window3.mainloop()