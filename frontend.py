import tkinter as tk
import sys
import backend


class Front(object):
    def __init__(self, window):
        # conect to the backend
        self.bk = backend.Back()

        # here we will add all the front end widgets (names, buttons, etc)
        self.w = window
        self.w.title("Movie Database App")
        self.w.geometry("1000x600")
        self.font = ("Arial", 14)
        self.font2 = ("Arial", 10)

        # lets add the widgets
        self.title_info = tk.Label(master=self.w, text="Title", width=15, font=self.font, anchor=tk.W)
        self.title_info.grid(row=0, column=0, pady=(30, 0), padx=(30,0))

        self.title_text = tk.StringVar() # this is just to hold the editable text
        self.title = tk.Entry(master=self.w, font=self.font, textvariable=self.title_text)
        self.title.grid(row=0, column=1, padx=30, pady=(30, 0))

        self.year_info = tk.Label(master=self.w, text="Year", width=15, font=self.font, anchor=tk.W)
        self.year_info.grid(row=0, column=2, pady=(30, 0))

        self.year_text = tk.StringVar() # this is just to hold the editable text
        self.year = tk.Entry(master=self.w, font=self.font, textvariable=self.year_text)
        self.year.grid(row=0, column=3, pady=(30, 0))

        self.director_info = tk.Label(master=self.w, text="Director", width=15, font=self.font, anchor=tk.W)
        self.director_info.grid(row=1, column=0, padx=(30,0))

        self.director_text = tk.StringVar() # this is just to hold the editable text
        self.director = tk.Entry(master=self.w, font=self.font, textvariable=self.director_text)
        self.director.grid(row=1, column=1, padx=30)

        self.lead_info = tk.Label(master=self.w, text="Actress/Actor", width=15, font=self.font, anchor=tk.W)
        self.lead_info.grid(row=1, column=2)

        self.lead_text = tk.StringVar() # this is just to hold the editable text
        self.lead = tk.Entry(master=self.w, font=self.font, textvariable=self.lead_text)
        self.lead.grid(row=1, column=3)

        # lets create the main display - the widget is called a listbox
        self.display = tk.Listbox(master=self.w, height=10, width=70, font=self.font2)
        self.display.grid(row=2, column=0, columnspan=2, rowspan=10, pady=50, padx=(30,0))
        self.display.bind("<<ListboxSelect>>", self.select_row)

        # add a scrollbar
        self.scroll = tk.Scrollbar(master=self.w)
        self.scroll.grid(row=2, column=2, sticky="nsw", rowspan=10, pady=50)
        #link the scroll to the ListBox:
        self.scroll.configure(command=self.display.yview)

        #button time!
        self.add = tk.Button(master=self.w, font=self.font, text="Add", width=10, command=self.add_entry)
        self.add.grid(row=2, column=3, pady=(50, 0))

        self.delete = tk.Button(master=self.w, font=self.font, text="Delete", width=10, command=self.delete_entry)
        self.delete.grid(row=3, column=3)

        self.exit = tk.Button(master=self.w, font=self.font, text="Exit", width=10, command=sys.exit)
        self.exit.grid(row=7, column=3)

    def select_row(self, event=None):
        pass

    def add_entry(self):
        # get the data from the Entries in the frontend
        title = self.title.get()
        year = int(self.year.get())
        director = self.director.get()
        lead = self.lead.get()
        # lets pass them to the backend
        self.bk.add_to_db(title, year, director, lead)
        self.show_all_database()

    def delete_entry(self):
        pass

    def show_all_database(self):
        rows = self.bk.get_all()
        for row in rows:
            # print in in the list
            self.display.insert(tk.END, row)


# always how you create a window
window = tk.Tk()
movie_app = Front(window)

# always how to keep looping a tkinter application
window.mainloop()





