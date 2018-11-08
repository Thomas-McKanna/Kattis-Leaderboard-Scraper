import http.client
from html.parser import HTMLParser

conn = http.client.HTTPSConnection("www.kattis.com", 443)
conn.request("GET", "https://open.kattis.com/universities/mst.edu")
response = conn.getresponse()

data = str(response.read())

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == "table":
            print("Found table!")
            print(attrs)

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass

parser = MyHTMLParser()
parser.feed(data)