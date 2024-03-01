import json

from bs4 import BeautifulSoup

html_doc = """<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""




soup = BeautifulSoup(html_doc, 'html.parser')

print(soup.find_all('a'))

all_links = soup.find_all("a")
data_save = []
for link in all_links:
    print(f' Це посилання {link.get("href")} на {link.text}')
    data = {
        "href": link.get("href"),
        "text": link.text
    }
    data_save.append(data)
    
with open("data_test.json", "w") as file:
    json.dump(data_save, file, indent=4)
