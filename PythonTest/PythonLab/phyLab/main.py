import requests
import lxml
import bs4
url = "http://10.103.4.10:8020/UI/model/Center/SelectECourseItem.html?id=934"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57',   'Cookie': 'ASP.NET_SessionId=slmswieazjbc3vh5u5w4k5ib'}

try:
    r = requests.get(url, headers=headers)
    r.encoding = "utf-8"
    soup = bs4.BeautifulSoup(r.text, "lxml")
    print(soup)

except IOError as e:
    print(str(e))
