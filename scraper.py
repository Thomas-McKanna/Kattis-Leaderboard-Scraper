import http.client
from html.parser import HTMLParser
from lxml import etree
from io import StringIO
from yattag import Doc

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

doc, tag, text, line = Doc().ttl()

# for alternating between line color
iter = 0

with tag('html'):
    with tag('head'):
        with tag('title'):
            text("Kattis Scores")
        doc.stag('link', rel="stylesheet", href="styles.css")
    with tag('body'):
        with tag('div', klass="datagrid"):
            with tag('table'):
                with tag('thead'):
                    with tag('tr'):
                        for s in ("Name", "Score"):
                            with tag('th'):
                                text(s)
                
                with tag('tbody'):
                    for person in nameAndScore:
                        if iter % 2 == 0:
                            with tag('tr'):
                                for d in (person[0], person[1]):
                                    with tag('td'):
                                        text(d)
                        else:
                            with tag('tr', klass="alt"):
                                for d in (person[0], person[1]):
                                    with tag('td'):
                                        text(d)
                        iter += 1

print("<!DOCTYPE html>")
print(doc.getvalue())

