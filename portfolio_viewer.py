import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter_toolbox import Dlabel
from yahoo_fin import stock_info as si
from budgeting_app import truncate
import numpy as np
import datetime
import pickle

def parse_stocks(text,mode):
	global stocks
	global stocks_loaded
	if mode=='remove': remove_stocks=[[]]
	start=True
	something_went_wrong=False
	last_char_comma=False
	if stocks_loaded: i2=len(stocks)
	else: i2=0
	i3=1
	#try:
	if True:
		for i in text:
			if stocks_loaded and start:
				if mode=='add':
					stocks.append([])
			if start: 
				stock=''
				stock+=i
				start=False	
			elif i==',': 
				if mode=='add':
					stocks[i2].append(int(stock_num))
					stocks.append([])
				else:
					remove_stocks[i2].append(int(stock_num))
					remove_stocks.append([])
				last_char_comma=True
				i2+=1
			elif i.isalpha(): stock+=i
			elif i==' ': 
				if last_char_comma==True:
					last_char_comma=False
				else: 
					if mode=='add': stocks[i2].append((stock.lower()))
					else: remove_stocks[i2].append((stock.lower()))
					stock=''
					stock_num=''
			elif i.isnumeric():
				stock_num+=i
				if i3==len(text): 
					if mode=='add': stocks[i2].append(int(stock_num))
					else: remove_stocks[i2].append(int(stock_num))
			else: something_went_wrong=True
			i3+=1

		if something_went_wrong: 
			stocks=[[]]
			messagebox.showinfo('Character Error', 'Make sure you have entered the stock\'s ticker,'+
			' followed by a space and the number of shares to be added/removed.\n Example: "AMZN 4, AAPL 5".\nYour current portfolio has been reset.')
		else:
			#deleting stocks
			del_list=[]
			if mode=='remove':
				i1=0
				for i_r in remove_stocks:
					i2=0
					for i_s in stocks:
						if i_r[0]==i_s[0]:
							i_s[1]=(i_s[1]-i_r[1])
							if i_s[1]<=0: del_list.append(i2)
						i2+=1
					i1+=1
				try: 
					for i in del_list: del stocks[i]
				except: messagebox.showinfo('Deleting Error','Something went wrong. Check for typos, or make sure you actually have the stock you think you have.')

			#error checking + printing stocks
			total=0
			i2=0
			del_list=[]
			now = datetime.datetime.now()
			# print('\n-------------------------------Portfolio-------------------------------\nPrices as of '+now.strftime("%m-%d-%Y %H:%M:%S"))
			for i in stocks: 
			 	price=si.get_live_price(i[0])
			 	if np.isnan(np.sum(price)): 
			 		messagebox.showinfo('Ticker Error','"'+i[0].upper()+'"" does not appear to be a real ticker. Check for typos or try looking up the company\'s ticker.'+
			 			'Your other stocks were still entered, so entering them again will double the number of stocks you have.')
			 		del_list.append(i2)
			 	# else: 
			 	# 	print('\n'+i[0].upper()+': $'+truncate(price,2)+' x '+str(i[1])+' = $'+truncate((i[1]*price),2))
			 	# 	total+=i[1]*price
			 	i2+=1
			for i in del_list: del stocks[i]
			# print('\nTotal: $'+truncate(total,2))
			update_stocks()
	# except:
	# 	messagebox.showinfo('Error','Something went wrong. Check for typos, and make sure that you typed a space followed by a number after each ticker. If any'+
	# 		' stocks were printed out, the printed ones have been successfully entered.')

def update_stocks():
	global stocks
	if stocks==[[]]: messagebox.showinfo('You have no stocks!','You cannot view your stock prices if you have not entered any stocks.')
	else:
		try:
			now = datetime.datetime.now()
			total=0
			stock_print='Portfolio:\nPrices as of '+now.strftime("%m-%d-%Y %H:%M:%S")
			print('\n-------------------------------Portfolio-------------------------------\nPrices as of '+now.strftime("%m-%d-%Y %H:%M:%S"))
			for i in stocks:
				price=si.get_live_price(i[0])
				string=('\n'+i[0].upper()+': $'+truncate(price,2)+' x '+str(i[1])+' = $'+truncate((i[1]*price),2))
				print(string)
				stock_print+='\n'+string
				total+=i[1]*price
			print('\nTotal: $'+truncate(total,2))
			stock_print+=('\n\nTotal: $'+truncate(total,2))
			stock_view=Dlabel(window2,stock_print,2,3)
		except:
			messagebox.showinfo('Error','Something went wrong. Check for typos, and make sure that you typed a space followed by a number after each ticker. If any'+
				' stocks were printed out, the printed ones have been successfully entered. If you loaded this budget, try deleting it, making a new one, and saving that.')

def save_portfolio():
    global stocks
    file = open('portfolio','wb')
    pickle.dump(stocks,file)
    file.close()

def load_portfolio():
	global stocks
	global stocks_loaded
	stocks_loaded=True
	f_port=open('portfolio','rb')
	stocks=pickle.load(f_port)
	update_stocks()

def delete_portfolio():
	global stocks
	global delete_port_attemps
	if delete_port_attemps==0:
		messagebox.showinfo('ARE YOU SURE?','Deleting your portfolio will clear it and delete your saved portfolio as well.'+
			' If you really want to, press "OK" and then the "Delete Portfolio" button again')
		delete_port_attemps+=1
	else:
		messagebox.showinfo('Portfolio Deleted','Your portfolio was deleted.')
		stocks=[[]]
		save_portfolio()
		delete_port_attemps=0

#AMZN 4, AAPL 5, MYL 25
if __name__ == "__main__":
	global delete_port_attemps
	global stocks_loaded
	stocks_loaded=False
	delete_port_attemps=0
	stocks=[[]]
	window2=Tk()
	window2.title("Finance Helper-Portfolio Viewer")
	window2.geometry('1250x750')
	window2.option_add("*Font", "arial 12")

	#builds menu bars
	menu = Menu(window2)
	new_item = Menu(menu)
	new_item.add_command(label='Save Portfolio',command=lambda: save_portfolio())
	new_item.add_command(label='Load Portfolio',command=lambda: load_portfolio())
	menu.add_cascade(label='File', menu=new_item)
	window2.config(menu=menu)

	#builds GUI
	stock_directions = Label(window2,text=('Add or remove stocks from your portfolio by typing the stock\'s ticker, followed by a space and the number of shares to be added/removed.\n' +
		'To enter multiple at once, simply add a comma and one space between them.\n Example: "AMZN 4, AAPL 5"'))
	stock_directions.grid(column=2, row=1)
	stock_entry_box = Entry(window2,width=100)
	stock_entry_box.grid(column=2, row=2)
	add_stock = Button(window2,text='Add Stocks', command= lambda: parse_stocks(stock_entry_box.get(),'add'))
	add_stock.grid(column=1, row=3)
	remove_stock = Button(window2,text='Remove Stocks', command= lambda: parse_stocks(stock_entry_box.get(),'remove'))
	remove_stock.grid(column=0, row=3)
	remove_stock = Button(window2,text='Delete Portfolio', command= lambda: delete_portfolio())
	remove_stock.grid(column=0, row=4)
	update= Button(window2,text='Update Prices', command= lambda: update_stocks())
	update.grid(column=1, row=4)
	window2.mainloop()