import tkinter as tk
from tkinter import messagebox, PhotoImage, StringVar, Label, Listbox, Button, Scrollbar, Entry
from db import Database

db = Database('store.db')

class Application(tk.Frame):

	def __init__(self, master):

		super().__init__(master)

		self.master = master

		master.title('Part Manager')
		
		master.geometry('700x400')

		photo = PhotoImage(file='random_logo.png')
		master.iconphoto(False, photo)

		master.configure(bg="#42f5d7")

		self.create_widgets()

		self.selected_item=0

		self.populate_list()


	def create_widgets(self):

		self.part_label = Label(self.master, text="Part Name", font=('bold', 14), pady=20)
		self.part_label.grid(row=0, column=0, sticky=tk.W)
		self.part_text = StringVar()
		self.part_entry = Entry(self.master, textvariable=self.part_text)
		self.part_entry.grid(row=0, column=1)

		self.customer_text = StringVar()
		self.customer_label = Label(self.master, text="Customer Name", font=('bold', 14), pady=20)
		self.customer_label.grid(row=0, column=2, sticky=tk.W)
		self.customer_entry = Entry(self.master, textvariable=self.customer_text)
		self.customer_entry.grid(row=0, column=3)

		self.retailer_text = StringVar()
		self.retailer_label = Label(self.master, text="Retailer", font=('bold', 14), pady=20)
		self.retailer_label.grid(row=1, column=0, sticky=tk.W)
		self.retailer_entry = Entry(self.master, textvariable=self.retailer_text)
		self.retailer_entry.grid(row=1, column=1)

		self.price_text = StringVar()
		self.price_label = Label(self.master, text="Price", font=('bold', 14), pady=20)
		self.price_label.grid(row=1, column=2, sticky=tk.W)
		self.price_entry = Entry(self.master, textvariable=self.price_text)
		self.price_entry.grid(row=1, column=3) 

		#parts list listbox

		self.parts_list = Listbox(self.master, height=10, width=80, border=0)
		self.parts_list.grid(row=3, column=0, columnspan=3, rowspan=6, pady=20, padx=20)


		self.scroll_bar = Scrollbar(self.master)
		self.scroll_bar.grid(row=3, column=3, sticky='ns', rowspan=6)

		#connect scroll and listbox

		self.parts_list.configure(yscrollcommand=self.scroll_bar.set)
		self.scroll_bar.configure(command=self.parts_list.yview)

		self.parts_list.bind('<<ListboxSelect>>', self.select_item)

		#Buttons

		self.add_button = Button(self.master, text="Add Part", width=12, command=self.add_item)
		self.add_button.grid(row=2, column=0, pady=20)

		self.remove_button = Button(self.master, text="Remove Part", width=12, command=self.remove_item)
		self.remove_button.grid(row=2, column=1, pady=20)

		self.update_button = Button(self.master, text="Update Part", width=12, command=self.update_item)
		self.update_button.grid(row=2, column=2, pady=20)

		self.clear_button = Button(self.master, text="Clear Text", width=12, command=self.clear_item)
		self.clear_button.grid(row=2, column=3, pady=20)


	def populate_list(self):

		self.parts_list.delete(0,tk.END)

		for row in db.fetch():

			self.parts_list.insert(tk.END, row)


	def add_item(self):

		if(self.part_text.get() == '' or self.customer_text.get()=='' or self.retailer_text.get()=='' or self.price_text.get()==''):
			messagebox.showerror('Required Fields', "Please include all fields")

			return

		db.insert(self.part_text.get(), self.customer_text.get(), self.retailer_text.get(), self.price_text.get())

		self.parts_list.delete(0, tk.END)

		self.parts_list.insert(tk.END, (self.part_text.get(), self.customer_text.get(), self.retailer_text.get(), self.price_text.get()))

		self.clear_item()
		self.populate_list()


	def select_item(self, event):

		try:
			global selected_item

			index = self.parts_list.curselection()[0]

			self.selected_item = self.parts_list.get(index)

			# print(selected_item)

			self.part_entry.delete(0,tk.END)
			self.part_entry.insert(tk.END, self.selected_item[1])

			self.customer_entry.delete(0,tk.END)
			self.customer_entry.insert(tk.END, self.selected_item[2])

			self.retailer_entry.delete(0,tk.END)
			self.retailer_entry.insert(tk.END, self.selected_item[3])

			self.price_entry.delete(0, tk.END)
			self.price_entry.insert(tk.END, self.selected_item[4])
		except IndexError:
			pass


	def remove_item(self):
	# print('remove')

		db.remove(self.selected_item[0])

		self.clear_item()
		self.populate_list()


	def update_item(self):
	# print('update')

		if(self.part_text.get() == '' or self.customer_text.get()=='' or self.retailer_text.get()=='' or self.price_text.get()==''):
			messagebox.showerror('Required Fields', "Please include all fields")

			return

		db.update(self.selected_item[0], self.part_text.get(), self.customer_text.get(), self.retailer_text.get(), self.price_text.get())

		self.clear_item()
		self.populate_list()


	def clear_item(self):
	# print('clear')

		self.part_entry.delete(0,tk.END)

		self.customer_entry.delete(0,tk.END)

		self.retailer_entry.delete(0,tk.END)

		self.price_entry.delete(0, tk.END)


window = tk.Tk()
app = Application(master=window)
app.mainloop()