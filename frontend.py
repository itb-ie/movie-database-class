import tkinter as tk
import sys
import backend

import requests
from bs4 import BeautifulSoup
from pytube import YouTube
import os
import subprocess

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
        self.last_selected = 0

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
        self.show = tk.Button(master=self.w, font=self.font, text="Show All", width=10, command=self.show_all_database)
        self.show.grid(row=2, column=3, pady=(50, 0))

        self.add = tk.Button(master=self.w, font=self.font, text="Add", width=10, command=self.add_entry)
        self.add.grid(row=3, column=3, pady=(0, 0))

        self.delete = tk.Button(master=self.w, font=self.font, text="Delete", width=10, command=self.delete_entry)
        self.delete.grid(row=4, column=3)

        self.update = tk.Button(master=self.w, font=self.font, text="Update", width=10, command=self.update_entry)
        self.update.grid(row=5, column=3)

        self.search = tk.Button(master=self.w, font=self.font, text="Search", width=10, command=self.search_entry)
        self.search.grid(row=6, column=3)

        self.play = tk.Button(master=self.w, font=self.font, text="Trailer", width=10, command=self.play_trailer)
        self.play.grid(row=7, column=3)

        self.exit = tk.Button(master=self.w, font=self.font, text="Exit", width=10, command=sys.exit)
        self.exit.grid(row=8, column=3)

        # display the database
        self.show_all_database()

    def select_row(self, event=None):
        # first determine the row selected
        rows = self.display.curselection()
        print(rows)
        try:
            # get the line information:
            line = self.display.get(rows[0])
        except:
            return ()

        #fill in the selected information in the text boxes above
        self.title_text.set(line[1])
        self.year_text.set(line[2])
        self.director_text.set(line[3])
        self.lead_text.set(line[4])
        print(line)
        self.last_selected = line[0]
        return line

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
        line = self.select_row()
        # call the backend method to delete
        try:  # this is because there could be nothing selected, so we can not delete
            self.bk.del_from_db(line[0])
        except:
            pass
        self.show_all_database()

    def update_entry(self):
        # let's get the information from the GUI
        title = self.title.get()
        year = int(self.year.get())
        director = self.director.get()
        lead = self.lead.get()

        # call the backend to update the database
        self.bk.update_db(title, year, director, lead, self.last_selected)
        # we are all done, show the database
        self.show_all_database()

    def search_entry(self):
        title = self.title.get()
        year = self.year.get()
        director = self.director.get()
        lead = self.lead.get()
        rows = self.bk.search(title, year, director, lead)
        self.display.delete(0, tk.END)
        for row in rows:
            # print in in the list
            self.display.insert(tk.END, row)

    def show_all_database(self):
        rows = self.bk.get_all()
        self.display.delete(0, tk.END)
        for row in rows:
            # print in in the list
            self.display.insert(tk.END, row)

    def play_trailer(self):
        # we need to construct the query: title + year + "trailer"
        title = self.title.get()
        year = self.year.get()
        query = "{} {} trailer".format(title, year)
        print(query)

        # here comes the copy pasted part from youtube.py
        page = requests.get("http://google.com/search?hl=en&q={}".format(query))

        soup = BeautifulSoup(page.content, features="html.parser")
        print(soup.prettify())
        # we need to get the links from the page, the elements are under a href
        links = soup.find_all("a")

        for link in links:
            link_parsed = link.get("href")
            print(link_parsed)
            # from all the links, I just care about youtube links, and in particular the first one
            if "youtube" in link_parsed:
                print("My final link is:", link_parsed)
                break

        # because google is not giving us the nice link, we need to sanitize it:
        final_link = link_parsed.replace("/url?q=", "")
        sa_pos = final_link.find("&sa")
        final_link = final_link[0:sa_pos]
        final_link = final_link.replace("%3Fv%3D", "?v=")
        print(final_link)

        yt = YouTube(final_link)

        stream = yt.streams.get_highest_resolution()
        # save this stream
        stream.download("", "trailer")

        # lets add code to play it. This functionality is different between mac and win
        if tk.sys.platform == "win32": # we are on a windows platform
            os.startfile("trailer.mp4")
        else:
            # we assume Mac since we do not support linux yet
            subprocess.call(["open", "trailer.mp4"])



# always how you create a window
window = tk.Tk()
movie_app = Front(window)

# always how to keep looping a tkinter application
window.mainloop()





