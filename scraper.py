import http.client
from html.parser import HTMLParser
from lxml import etree
from io import StringIO
from yattag import Doc

# Open name.txt file for reading
with open('names.txt', 'r') as f:
    commaList = f.read()
    usernames = [username.strip() for username in commaList.split(',')]

# Connect to Kattis website
conn = http.client.HTTPSConnection("www.kattis.com", 443)

nameAndScore = []

# Get everyone's scores
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

# Sort by highest score
nameAndScore = sorted(nameAndScore, key=lambda kv: float(kv[1]), reverse = True)

# Load in previous scores for comparison
prevNameToScoreAndPos = {}
isPrev = True
try:
    with open('prev_scores.txt', 'r') as f:
        curr_row = f.readline()
        while (curr_row != ''):
            curr_row = curr_row[:-1] # remove newline
            curr_row_split = curr_row.split(',')
            prevNameToScoreAndPos[curr_row_split[1]] = (curr_row_split[0], curr_row_split[2])
            curr_row = f.readline()
except:
    isPrev = False


doc, tag, text, line = Doc().ttl()

# For alternating between line color
iter = 0

# Generate html table
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
                        for s in ("Position", "Name", "Score", "Status"):
                            with tag('th'):
                                text(s)

                with tag('tbody'):
                    for person in nameAndScore:
                        with tag('tr') if iter % 2 == 0 else tag('tr', klass="alt"):
                            with tag('td'):
                                text(iter + 1)
                            with tag('td'):
                                text(person[0])
                            with tag('td'):
                                text(person[1])
                            with tag('td'):
                                # Check to see if the person has moves up or down in list
                                # or has earned more than 10 points since last run
                                if isPrev:
                                    try:
                                        if int(prevNameToScoreAndPos[person[0]][0]) > nameAndScore.index(person) + 1:
                                            doc.stag('img', src="assets/img/green_up_arrow.png", height="25")
                                        elif int(prevNameToScoreAndPos[person[0]][0]) < nameAndScore.index(person) + 1:
                                            doc.stag('img', src="assets/img/red_down_arrow.png", height="25")
                                        elif float(prevNameToScoreAndPos[person[0]][1]) < float(person[1]):
                                            doc.stag('img', src="assets/img/green_circle.png", height="17")
                                        elif float(prevNameToScoreAndPos[person[0]][1]) == float(person[1]):
                                            doc.stag('img', src="assets/img/yellow_circle.png", height="25")

                                        if float(prevNameToScoreAndPos[person[0]][1]) <= float(person[1]) - 10:
                                            doc.stag('img', src="assets/fire.png", height="25")
                                    except:
                                        print("Error with the previous scores files. It has been overwritten with "
                                        "newest values. Please run the progam again.")
                        iter += 1

with open('output.html', 'w') as f:
    f.write("<!DOCTYPE html>" + doc.getvalue())

# Record scores for next time
iter = 1
with open('prev_scores.txt', 'w') as f:
    for person in nameAndScore:
        f.write(str(iter) + ',' + str(person[0]) + ',' + str(person[1]) + '\n')
        iter += 1
