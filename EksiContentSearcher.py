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

parser.add_argument('-t', '--title', type=str, required = True,
                    help='Title or Url of title')

parser.add_argument('-s', '--search', type=str, required = True,
                    help='What we are searching in this title')

parser.add_argument('-f', '--fast', action='store_true', default = False,
                    help='You should type pip3 install lxml to enable this.')

parser.add_argument('--txt', action='store_false', default = True,
                    help='outputs a txt file instead of html file.')

parser.add_argument('--dark', action='store_true', default = False,
                    help='outputs dark backgrounded html file.')


args = parser.parse_args()

if len(args.search) < 2:
    print("Search word must contain at least 2 character.")
    exit(-1)

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
r = requests.get(url + str(pageNumber), headers = headers)
soup = BeautifulSoup(r.content, parser)
pageCount = 0
try:
    pageCount = soup.select("#topic > div.clearfix.sub-title-container > div.pager")[0].get("data-pagecount")
except:
    print("Title is not found! Write title with as you see in title with turkish letters or use links.")
    print('NOTE: Single page titles are judged as "Title is not found!"')
    exit(-1)
totalPageCount = int (pageCount)

html = args.txt
import re
def handleTitle(string):
    old = re.findall(r'title="\(bkz:[^()]*\)"', string)#Think numbers
    if len(old) == 0: return string
    new = re.sub(" ","",old[0])
    result = string.replace(old[0],new)
    return result

def handleDataquery(string):
    old = re.findall(r'data-query="[a-zA-ZıöçşüğİÖŞÇÜĞ ]*"', string) #Think numbers
    if len(old) == 0: return string
    new = re.sub(" ","",old[0])
    result = string.replace(old[0],new)
    return result

def eveluateEntry(string):
    string = handleTitle(string)
    return re.sub(r'(?<!(data-query="|..........q=|title="\(bkz:)|...........-|.........../|........www\.)' + searchContent + r'(?!".*>)', '<mark style:"display:inline;">' + searchContent + '</mark>', string)
    
while pageNumber <= totalPageCount:
    r = requests.get(url + str(pageNumber), headers = headers)
    print("We are scanning page ", pageNumber, "over pages :", str(totalPageCount), "\b\r", end="")
    pageNumber = pageNumber + 1
    soup = BeautifulSoup(r.content, parser)
    while contentNumber < 14: # Last entry is numbered as 13.
        try:
            if html:
                entry = soup.select("#entry-item-list > li:nth-child(" + str(contentNumber) +") > div.content")[0].prettify()
            else:
                entry = soup.select("#entry-item-list > li:nth-child(" + str(contentNumber) +") > div.content")[0].text
            if searchContent in entry and not html:
                sb += "Page number : " + str(pageNumber - 1) + "\n\n" + entry + "\n"
            elif searchContent in entry and html:
                sb += "<hr>Page number : " + str(pageNumber - 1) + eveluateEntry(entry) + "<br>"
            contentNumber = contentNumber + 1
        except IndexError:
            contentNumber = contentNumber + 1
            pass
    contentNumber = 2


print("Done!                                     \n") # Clear line


def changeHtmlFormat(text, searchContent):
    color = ""
    if args.dark == True:
        color = "#4E1D1D"
    else:
        color = "#ffffff"
    text = handleTitle(text)
    text = handleDataquery(text)
    li = text.split(" ")
    res = """<!DOCTYPE html><html lang="en">
    <head>
        <title>Result</title>
        <style id="styling">
            body{
                max-width: 700px;
                margin:auto;
                background-color: """ + color + """
            }
            *::selection{
                /*color: red;*/
                background-color: #B3A9E1;
                /*text-shadow: 2px 2px 20px yellow;*/
                text-shadow: 1px 1px 4px #113706;
            }
        </style>
        <script>
            function invertColor(hex, bw) {
                if (hex.indexOf('#') === 0) {
                    hex = hex.slice(1);
                }
                // convert 3-digit hex to 6-digits.
                if (hex.length === 3) {
                    hex = hex[0] + hex[0] + hex[1] + hex[1] + hex[2] + hex[2];
                }
                if (hex.length !== 6) {
                    throw new Error('Invalid HEX color.');
                }
                var r = parseInt(hex.slice(0, 2), 16),
                    g = parseInt(hex.slice(2, 4), 16),
                    b = parseInt(hex.slice(4, 6), 16);
                if (bw) {
                    // http://stackoverflow.com/a/3943023/112731
                    return (r * 0.299 + g * 0.587 + b * 0.114) > 186
                        ? '#000000'
                        : '#FFFFFF';
                }
                // invert color components
                r = (255 - r).toString(16);
                g = (255 - g).toString(16);
                b = (255 - b).toString(16);
                // pad each with zeros and return
                return "#" + padZero(r) + padZero(g) + padZero(b);
            }

            function padZero(str, len) {
                len = len || 2;
                var zeros = new Array(len).join('0');
                return (zeros + str).slice(-len);
            }

            function rgbToHex(color) {
                color = ""+ color;
                if (!color || color.indexOf("rgb") < 0) {
                    return;
                }

                if (color.charAt(0) == "#") {
                    return color;
                }

                var nums = /(.*?)rgb\((\d+),\s*(\d+),\s*(\d+)\)/i.exec(color),
                    r = parseInt(nums[2], 10).toString(16),
                    g = parseInt(nums[3], 10).toString(16),
                    b = parseInt(nums[4], 10).toString(16);

                return "#"+ (
                    (r.length == 1 ? "0"+ r : r) +
                    (g.length == 1 ? "0"+ g : g) +
                    (b.length == 1 ? "0"+ b : b)
                );
            }

                    
            document.addEventListener("DOMContentLoaded", function(){
                let colorPicker = document.querySelector("#bgcolor");
                let marker = document.querySelector("#marking");
                let cssFile = document.querySelector("#styling").sheet;
                
                bgColor = getComputedStyle(document.querySelector("body")).backgroundColor
                
                
                colorPicker.value = rgbToHex(bgColor)
                document.querySelector("body").style["color"] = invertColor(colorPicker.value);
                
                colorPicker.addEventListener("input", ()=>{
                    document.querySelector("body").style["background-color"] = colorPicker.value;
                    document.querySelector("body").style["color"] = invertColor(colorPicker.value);
                });
                let bool = false;
                marker.addEventListener("change", ()=>{
                    if(marker.checked == true){
                        if (bool) cssFile.deleteRule(0);
                        bgColor = getComputedStyle(document.querySelector("body")).backgroundColor
                        let textColor = getComputedStyle(document.querySelector("body")).color
                        let color = rgbToHex(bgColor);
                        let color2 = rgbToHex(textColor);
                        let style = `mark{background-color:${color};color:${color2}}`
                        cssFile.insertRule(style, 0);
                        bool = true;
                    }else{
                        cssFile.deleteRule(0);
                        let style = `mark{background-color:yellow;color:black}`
                        cssFile.insertRule(style, 0);
                    }
                });
                
            });

        </script>
    </head>
    <body>

    <label for="bgcolor">Select your background-color:</label>
    <input type="color" id="bgcolor" name="bgcolor" value="#ffffff"><br><br>

    <label for="marking">disable marking:</label>
    <input type="checkbox" id="marking" name="marking" ><br><br>

    """
    
    for item in li:
        if 'href="' in item and not 'href="ht' in item:
            a = item.split("/", 1)
            res += a[0] + "https://eksisozluk.com/" + a[1] + " "
        else:
            res += item + " "
    
    res += """</body></html> """
    return res



if html:
    f = open(title + "-" + args.search + ".html", "w")
    f.write(changeHtmlFormat(sb, searchContent))
    f.close()
else:
    f = open(title + "-" + args.search + ".txt", "w")
    f.write(sb)
    f.close()

endTime = current_milli_time()

print("This process last for " + str ( ( endTime - startTime ) / 1000.0) )
