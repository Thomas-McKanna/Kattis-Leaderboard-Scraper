import http.client
from html.parser import HTMLParser
from lxml import etree
from io import StringIO

conn = http.client.HTTPSConnection("www.kattis.com", 443)
conn.request("GET", "https://open.kattis.com/universities/mst.edu")
response = conn.getresponse()

data = str(response.read())

decodedData = bytes(data, "utf-8").decode("unicode_escape") 

parser = etree.HTMLParser()

tree   = etree.parse(StringIO(data), parser)

result = etree.tostring(tree.getroot(), method="html")

print(result)
