from bs4 import BeautifulSoup
import requests

import argparse
import time

def current_milli_time():
    return round(time.time() * 1000)

startTime = current_milli_time()

def changeTrwordToEnWord(word):
    word = word.split(".", 1)
    a = word[1].replace("ç", "c").replace("ö", "o").replace("ü", "u").replace("ş", "s").replace("ı", "i").replace("ğ", "g").replace("'", "").replace(".", "-")
    return word[0] + "." + a

# Instantiate the parser
parser = argparse.ArgumentParser(description='Optional app description')

parser.add_argument('-t', '--title', type=str,
                    help='Title or Url of title')

parser.add_argument('-s', '--search', type=str, 
                    help='What we are searching in this title')

parser.add_argument('-f', '--fast', action='store_true', default = False,
                    help='You shoudl type pip3 install lxml to enable this')


args = parser.parse_args()

parser = "html.parser"
if(args.fast == True):
    parser = "lxml"

print("parser is :", parser)

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
    #print("https://eksisozluk.com/?q=" + args.title)
    r = requests.get("https://eksisozluk.com/?q=" + args.title, headers = headers)
    soup = BeautifulSoup(r.content, parser)
    dataNumber = soup.select("#title")[0].get("data-id")
    link ="https://eksisozluk.com/"+ args.title.replace(" ", "-") + "--" + str(dataNumber) + "?p="
    url = changeTrwordToEnWord(link)


pageNumber = 1
contentNumber = 2

searchContent = args.search

sb = ""

# Getting total page count
#print("url is : ", url)
r = requests.get(url + str(pageNumber), headers = headers)
soup = BeautifulSoup(r.content, parser)
pageCount = 0
try:
    pageCount = soup.select("#topic > div.clearfix.sub-title-container > div.pager")[0].get("data-pagecount")
except:
    print("Title is not found! Write title with as you see in title with turkish letters or use links.")
    exit(-1)
totalPageCount = int (pageCount)


while pageNumber <= totalPageCount:
    r = requests.get(url + str(pageNumber), headers = headers)
    print("We are scanning page ", pageNumber, "over pages :", str(totalPageCount), "\b\r", end="")
    pageNumber = pageNumber + 1
    soup = BeautifulSoup(r.content, parser)
    while contentNumber < 14: # Last entry is numbered as 13.
        try:
            entry = soup.select("#entry-item-list > li:nth-child(" + str(contentNumber) +") > div.content")[0].text
            if searchContent in entry:
                sb += "Page number : " + str(pageNumber - 1) + "\n\n" + entry + "\n"
            contentNumber = contentNumber + 1
        except IndexError:
            contentNumber = contentNumber + 1
            pass
    contentNumber = 2



print("Done!                                     \n") # Clear line

print("Result is:\n")
print(sb)

f = open(title + "-" + args.search + ".txt", "w")
f.write(sb)
f.close()

endTime = current_milli_time()

print("This process last for " + str ( ( endTime - startTime ) / 1000.0) )
