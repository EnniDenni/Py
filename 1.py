import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

URL_TEMPLATE = "https://shazoo.ru/tags/105/movies"
r = requests.get(URL_TEMPLATE)

soup = bs(r.text, "html.parser")
titles = soup.find_all('div', class_='flex flex-col gap-2 py-6 first:pt-0')
hrefs = []
for i in titles:
    hrefs.append(i.find_all("a")[2].attrs["href"])
    
for href in hrefs: 
   r = requests.get(href)
   soup = bs(r.text, "html.parser")
   h1 = soup.find_all('h1', class_='sm:max-w-4xl text-xl sm:text-3xl leading-tight font-bold break-words dark:text-gray-300')[0].text
   print(h1)
   
   img = soup.find_all("img",class_="w-full rounded-md")[0].attrs["src"]
   print(img)
   textp = soup.find_all("p")[0]
   print(textp)

URL_TEMPLATE = "https://shazoo.ru/tags/419/games"
r = requests.get(URL_TEMPLATE)

soup = bs(r.text, "html.parser")
titles = soup.find_all('div', class_='flex flex-col gap-2 py-6 first:pt-0')
hrefs = []
for i in titles:
    hrefs.append(i.find_all("a")[2].attrs["href"])
    
for href in hrefs: 
   r = requests.get(href)
   soup = bs(r.text, "html.parser")
   h1 = soup.find_all('h1', class_='sm:max-w-4xl text-xl sm:text-3xl leading-tight font-bold break-words dark:text-gray-300')[0].text
   print(h1)
   
   img = soup.find_all("img",class_="w-full rounded-md")[0].attrs["src"]
   print(img)
   textp = soup.find_all("p")[0]
   print(textp)