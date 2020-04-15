import tkinter as tk
from tkinter import *
from tkinter_toolbox import Dlabel
from yahoo_fin import stock_info as si
from budgeting_app import truncate

def parse_stocks(text):
	stocks=[[]]
	start=True
	something_went_wrong=False
	last_char_comma=False
	i2=0
	i3=1
	for i in text:
		if start: 
			stock=''
			stock+=i
			start=False
		elif i==',': 
			stocks[i2].append(int(stock_num))
			stocks.append([])
			last_char_comma=True
			i2+=1
		elif i.isalpha(): stock+=i
		elif i==' ': 
			if last_char_comma==True:
				last_char_comma=False
			else: 
				stocks[i2].append((stock.lower()))
				stock=''
				stock_num=''
		elif i.isnumeric():
			stock_num+=i
			if i3==len(text): stocks[i2].append(int(stock_num))
		else: something_went_wrong=True
		i3+=1

	if something_went_wrong: messagebox.showinfo('Character Error', 'Make sure you have entered the stock\'s ticker,'+
		' followed by a space and the number of shares to be added/removed.\n Example: "AMZN 4, AAPL 5".')
	print(stocks)

	for i in stocks: 
	 	price=si.get_live_price(i[0])
	 	print('\n'+i[0].upper()+': $'+truncate(price,2)+' x '+str(i[1])+' = $'+truncate((i[1]*price),2))

#AMZN 4, AAPL 5, MYL 25
if __name__ == "__main__":
	window2=Tk()
	window2.title("Finance Helper-Portfolio Viewer")
	window2.geometry('1080x720')
	#window2.option_add("*Font", "arial 12")

	stock_directions = Label(window2,text=('Add or remove stocks from your portfolio by typing the stock\'s ticker, followed by a space and the number of shares to be added/removed.' +
		'To enter multiple at once, simply add a comma and one space between them.\n Example: "AMZN 4, AAPL 5"'))
	stock_directions.grid(column=1, row=1)
	stock_entry_box = Entry(window2,width=180)
	stock_entry_box.grid(column=1, row=2)
	add_stock = Button(window2,text='Add Stocks', command= lambda: parse_stocks(stock_entry_box.get()))
	add_stock.grid(column=2, row=2)
	
	window2.mainloop()