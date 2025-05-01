import requests
import lxml
import bs4
url = "https://www.lymone.cc"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47'}

try:
    r = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    for child in soup.article.next_siblings:
        for a in child.header:
            print(a)
except IOError as e:
    print(str(e))
