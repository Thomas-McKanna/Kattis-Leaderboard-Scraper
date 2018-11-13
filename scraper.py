import http.client
from html.parser import HTMLParser
from lxml import etree
from io import StringIO

# Open name.txt file for reading
f = open('names.txt', 'r')
commaList = f.read()
usernames = [username.strip() for username in commaList.split(',')]

# Connect to Kattis website
conn = http.client.HTTPSConnection("www.kattis.com", 443)

nameAndScore = []

for username in usernames:
    conn.request("GET", "https://open.kattis.com/users/" + username)
    response = conn.getresponse()
    
    data = str(response.read())

    decodedData = bytes(data, "utf-8").decode("unicode_escape") 

    decodedString = str(decodedData)

    parser = etree.HTMLParser()

    tree   = etree.parse(StringIO(decodedString), parser)

    root = tree.getroot()

    for element in root.iter("h1"):
        name = element.text

    td = [element.text for element in root.iter("td")]

    nameAndScore.append((name.strip(), td[-1]))

    """
    for element in root.iter():
        print(element.tag, " ", element.text)

    print(username)
    input()
    """

nameAndScore = sorted(nameAndScore, key=lambda kv: float(kv[1]), reverse = True)
for x in nameAndScore:
    print(x[0], ": ", x[1])