import requests
from bs4 import BeautifulSoup

class NewsService:
    BASE_URL = "https://news.google.com/search"

    def __init__(self, timeout=10):
        self.timeout = timeout
        self.headers = {
            "User-Agent": "Mozilla/5.0"
        }

    def fetch(self, query="technology", limit=5):
        params = {
            "q": query,
            "hl": "en-IN",
            "gl": "IN",
            "ceid": "IN:en"
        }

        res = requests.get(
            self.BASE_URL,
            params=params,
            headers=self.headers,
            timeout=self.timeout
        )
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "html.parser")

        results = []

        for item in soup.select("a.DY5T1d")[:limit]:
            title = item.text.strip()

            # fix relative URL
            raw_link = item.get("href")
            full_link = "https://news.google.com" + raw_link[1:]

            # resolve real article URL
            real_url = self._resolve_redirect(full_link)

            results.append({
                "title": title,
                "url": real_url
            })

        return results

    def _resolve_redirect(self, url):
        try:
            res = requests.get(url, headers=self.headers, timeout=self.timeout, allow_redirects=True)
            return res.url
        except:
            return url

    def fetch_full_content(self, url):
        try:
            res = requests.get(url, headers=self.headers, timeout=self.timeout)
            soup = BeautifulSoup(res.text, "html.parser")

            paragraphs = soup.find_all("p")
            content = " ".join(p.text for p in paragraphs[:10])

            return content.strip()
        except:
            return ""