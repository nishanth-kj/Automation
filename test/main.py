import requests
from bs4 import BeautifulSoup
import re

url = "https://x.com"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9"
}

res = requests.get(url, headers=headers)

soup = BeautifulSoup(res.text, "html.parser")

mainjs_link = None

for link in soup.find_all("link", {"rel": "preload"}):
    href = link.get("href")
    if href and "main" in href:
        mainjs_link = href
        print("main.js:", href)


if mainjs_link:
    mainjs_res = requests.get(mainjs_link,headers=headers)

query_id = (m.group(1) if (m := re.search(r'\{queryId:"([^"]+)",operationName:"CreateTweet"', mainjs_res.text))else None)

print(query_id)

