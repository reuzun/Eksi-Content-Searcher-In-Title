from bs4 import BeautifulSoup
import requests

import argparse

# Instantiate the parser
parser = argparse.ArgumentParser(description='Optional app description')

parser.add_argument('-t', '--title', type=str,
                    help='Title or Url of title')

parser.add_argument('-s', '--search', type=str, 
                    help='What we are searching in this title')

args = parser.parse_args()

headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})

title = args.title

# Means its a link
if "htt" and ".com" in args.title:
    link = args.title.split("?")
    link = link[0] + "?p="
    url = link

    # Adjusting title for setting file name.
    link = link.split("/")[3].split("-")
    title = link[0]
    
else: #Means its just a title
    r = requests.get("https://eksisozluk.com/?q=" + args.title, headers = headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    dataNumber = soup.select("#title")[0].get("data-id")
    link ="https://eksisozluk.com/"+ args.title + "--" + str(dataNumber) + "?p="
    url = link


pageNumber = 1
contentNumber = 2

searchContent = args.search

sb = ""

# Getting total page count
r = requests.get(url + str(pageNumber), headers = headers)
soup = BeautifulSoup(r.content, 'html.parser')
pageCount = soup.select("#topic > div.clearfix.sub-title-container > div.pager")[0].get("data-pagecount")
totalPageCount = int (pageCount)


while pageNumber <= totalPageCount:
    r = requests.get(url + str(pageNumber), headers = headers)
    print("We are scanning page ", pageNumber, "over pages :", str(totalPageCount), "\b\r", end="")
    pageNumber = pageNumber + 1

    while contentNumber < 25:
        try:
            soup = BeautifulSoup(r.content, 'html.parser')
            entry = soup.select("#entry-item-list > li:nth-child(" + str(contentNumber) +") > div.content")[0].text
            if searchContent in entry:
                sb += "Page number : " + str(pageNumber - 1) + "\n\n" + entry + "\n"
            contentNumber = contentNumber + 1
        except IndexError:
            contentNumber = contentNumber + 1
            pass
    contentNumber = 2
print("Done!\n")

print("Result is:\n")
print(sb)

f = open(title + "-" + args.search + ".txt", "w")
f.write(sb)
f.close()
