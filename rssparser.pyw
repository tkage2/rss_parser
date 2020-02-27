import feedparser
import tkinter as tk
from tkinter import *
import webbrowser
import time
from threading import Thread


# Main window	
class MainApp(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		
		self.urls = []
		self.item_list = []
		self.listbox_main = Listbox(master, width=70, height=25)
		self.listbox_main.bind('<Double-Button-1>', self.on_click)

		self.btn_editsrc = Button(master, text="Edit sources", width=5, command=self.open_src_edit_window)
		self.btn_editsrc.pack(fill=X)
		self.listbox_main.pack()
		self.refresh()

	
		
		
	def on_click(self, event):
		link = self.item_list[self.listbox_main.curselection()[0]]
		webbrowser.open(link['link'])
		
		
	def refresh(self):
		self.listbox_main.delete(0, 'end')
		self.item_list.clear()
		for x in self.urls:
			feed = feedparser.parse(x)
			for item in feed['items']:

				self.item_list.append(item)
				self.listbox_main.insert('end', item['title'])
		self.listbox_main.bind('<Double-Button-1>', self.on_click)
		self.listbox_main.pack()
	
	
	def open_src_edit_window(self):
		SourcesWindow(tk.Toplevel(self.master), self)
		
	
# Window for sources	
class SourcesWindow(tk.Frame):
	def __init__(self, master, main_app):
		tk.Frame.__init__(self, master)
		
		self.master.title("Sources")
		self.main_app = main_app
		
		self.lb_sources = Listbox(master, width=50, height=20)
		self.btn_remove = Button(master, text="Remove source", width=15, command=lambda: self.remove_source(self.lb_sources.curselection()[0]))
		self.btn_add = Button(master, text="Add source", width=15, command=lambda: self.add_source())
		self.btn_save = Button(master, text="Save", width=15, command=lambda: self.save_sources())
	
		self.lb_sources.pack()
		self.btn_add.pack(side='left')
		self.btn_remove.pack(side='left')
		self.btn_save.pack(side='left')
		
		self.refresh_sources()
		
		
	def refresh_sources(self):
		self.lb_sources.delete(0, 'end')
		for url in self.main_app.urls:
			self.lb_sources.insert('end', url)
			
	
	
	def add_source(self):
		InputWindow(tk.Toplevel(self.master), self)
	
	
	def remove_source(self, input):
		index = self.lb_sources.curselection()[0]
		del self.main_app.urls[index]
		self.refresh_sources()
	
	def save_sources(self):
		self.main_app.refresh()
		self.master.destroy()
		

# Window for adding sources.		
class InputWindow(tk.Frame):
	def __init__(self, master, edit_window):
		self.edit_window = edit_window
		tk.Frame.__init__(self, master)
		self.entry_input = Entry(master)
		self.ok_btn	= Button(master, text="OK", command=lambda: self.add_source_to_urls(self.entry_input.get()))
		self.entry_input.pack()
		self.ok_btn.pack()

	def add_source_to_urls(self, input):
		self.edit_window.main_app.urls.append(input)
		self.edit_window.refresh_sources()
		self.master.destroy()
		
	
def main():
	master = Tk()
	master.title("RSS")
	app = MainApp(master)
	master.after(10000000, app.refresh) # Built-in callback-function to refresh listbox_main after mainloop, timer added in milliseconds.
	master.mainloop()
	
if __name__ == '__main__':
	main()
	






	