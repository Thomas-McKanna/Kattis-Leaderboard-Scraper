import http.client

conn = http.client.HTTPSConnection("www.kattis.com", 443)
conn.request("GET", "https://open.kattis.com/universities/mst.edu")