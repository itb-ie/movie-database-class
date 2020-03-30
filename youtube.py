'''
Master Plan:
Steps:
1. Do a google search
2. Get the youtube link from the google search - done
3. Go to youtube and download the movie - done
4. Save the movie on my harddrive - done
5. Play the movie -
6. we can delete it when we are done!
7. !PROFIT!
'''

# we need to import requests library
import requests
from bs4 import BeautifulSoup
from pytube import YouTube
import tkinter as tk
import os
import subprocess

query = "the godfather trailer"


page = requests.get("http://google.com/search?hl=en&q={}".format(query))

#print(page.content)
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
for stream in yt.streams:
    print(stream)


stream = yt.streams.get_highest_resolution()
# save this stream
stream.download("", "trailer")

# lets add code to play it. This functionality is different between mac and win
if tk.sys.platform == "win32": # we are on a windows platform
    os.startfile("trailer.mp4")
else:
    # we assume Mac since we do not support linux yet
    subprocess.call(["open", "trailer.mp4"])






