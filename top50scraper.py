import http.client
from html.parser import HTMLParser
from lxml import etree
from io import StringIO

conn = http.client.HTTPSConnection("www.kattis.com", 443)
conn.request("GET", "https://open.kattis.com/universities/mst.edu")
response = conn.getresponse()

data = str(response.read())

decodedData = bytes(data, "utf-8").decode("unicode_escape") 

decodedString = str(decodedData)

parser = etree.HTMLParser()

tree   = etree.parse(StringIO(decodedString), parser)

root = tree.getroot()

names = []
scores = {}

# Scraping the names
NAME_SKIP = 13
NAME_OFFSET = 5
iter = 0
for element in root.iter("a"):
    if (iter < NAME_SKIP):
        pass
    else:
        if type(element.text) is str:
            split_name = element.text.split(' ')
            if len(split_name) > 1 and split_name[0] != "United" and split_name[0] != "Support":
                names.append(' '.join(split_name))
    iter += 1

# Scraping the scores
SCORE_SKIP = 4
SCORE_OFFSET = 4
iter = 0
count = 0
for element in root.iter("td"):
    if (iter < SCORE_SKIP):
        pass
    else:
        if ((iter - SCORE_SKIP + 1) % SCORE_OFFSET == 0):
            scores[names[count]] = element.text
            count += 1
    iter += 1

for name in names:
    print(name, ':', scores[name])