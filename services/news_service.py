import requests
from bs4 import BeautifulSoup
from utils.logger import logger

class NewsService:
    def __init__(self, timeout=10):
        self.timeout = timeout
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def fetch(self, query="trending", limit=20):
        logger.info(f"Scraper: Starting global fetch for query: '{query}'")
        all_results = []
        
        # 1. Google News
        try:
            res = self.fetch_google(query, limit=5)
            logger.info(f"Scraper: Google News returned {len(res)} items")
            all_results.extend(res)
        except Exception as e:
            logger.error(f"Scraper: Google News error: {e}")

        # 2. Reddit
        try:
            res = self.fetch_reddit(query, limit=5)
            logger.info(f"Scraper: Reddit returned {len(res)} items")
            all_results.extend(res)
        except Exception as e:
            logger.error(f"Scraper: Reddit error: {e}")

        # 3. Bing News
        try:
            res = self.fetch_bing(query, limit=5)
            logger.info(f"Scraper: Bing News returned {len(res)} items")
            all_results.extend(res)
        except Exception as e:
            logger.error(f"Scraper: Bing News error: {e}")

        # 4. DuckDuckGo
        try:
            res = self.fetch_duckduckgo(query, limit=5)
            logger.info(f"Scraper: DuckDuckGo returned {len(res)} items")
            all_results.extend(res)
        except Exception as e:
            logger.error(f"Scraper: DuckDuckGo error: {e}")

        # Remove duplicates by URL
        seen_urls = set()
        unique_results = []
        for res in all_results:
            url = res["url"]
            if url not in seen_urls:
                unique_results.append(res)
                seen_urls.add(url)
        
        logger.info(f"Scraper: Fetch complete. Total unique items: {len(unique_results)}")
        return unique_results[:limit]

    def fetch_google(self, query, limit=5):
        url = "https://news.google.com/search"
        params = {"q": query, "hl": "en-IN", "gl": "IN", "ceid": "IN:en"}
        res = requests.get(url, params=params, headers=self.headers, timeout=self.timeout)
        soup = BeautifulSoup(res.text, "html.parser")
        
        results = []
        articles = soup.select("article")
        for article in articles[:limit]:
            a_tag = article.select_one("a.JtKRv") or article.select_one('a[href^="./read"]')
            if not a_tag: continue
            
            title = a_tag.text.strip()
            logger.debug(f"Found on Google: {title[:50]}...")
            
            raw_link = a_tag.get("href")
            full_link = "https://news.google.com" + raw_link[1:]
            
            img_tag = article.select_one("img")
            img_url = img_tag.get("src") if img_tag else None
            if img_url and img_url.startswith("/"):
                img_url = "https://news.google.com" + img_url

            results.append({
                "title": title, 
                "url": full_link, 
                "source": "Google News",
                "image_url": img_url
            })
        return results

    def fetch_reddit(self, query, limit=5):
        subreddits = ["worldnews", "news", "technology"]
        results = []
        for sub in subreddits:
            try:
                url = f"https://www.reddit.com/r/{sub}/top.json?limit=3&t=day"
                headers = {"User-Agent": "MemeGeneratorBot/1.0"}
                res = requests.get(url, headers=headers, timeout=self.timeout)
                data = res.json()
                for post in data["data"]["children"]:
                    p = post["data"]
                    if p.get("stickied"): continue
                    logger.debug(f"Found on Reddit (r/{sub}): {p['title'][:50]}...")
                    results.append({
                        "title": p["title"],
                        "url": f"https://reddit.com{p['permalink']}",
                        "source": f"Reddit (r/{sub})",
                        "image_url": p.get("thumbnail") if p.get("thumbnail") not in ["self", "default", "nsfw"] else None
                    })
            except: continue
        return results

    def fetch_bing(self, query, limit=5):
        url = "https://www.bing.com/news/search"
        params = {"q": query}
        res = requests.get(url, params=params, headers=self.headers, timeout=self.timeout)
        soup = BeautifulSoup(res.text, "html.parser")
        results = []
        for card in soup.select(".news-card")[:limit]:
            a_tag = card.select_one("a.title")
            if not a_tag: continue
            title = a_tag.text.strip()
            logger.debug(f"Found on Bing: {title[:50]}...")
            results.append({
                "title": title,
                "url": a_tag.get("href"),
                "source": "Bing News",
                "image_url": None
            })
        return results

    def fetch_duckduckgo(self, query, limit=5):
        url = "https://html.duckduckgo.com/html/"
        params = {"q": f"{query} news"}
        res = requests.post(url, data=params, headers=self.headers, timeout=self.timeout)
        soup = BeautifulSoup(res.text, "html.parser")
        results = []
        for item in soup.select(".result__body")[:limit]:
            a_tag = item.select_one(".result__a")
            if not a_tag: continue
            title = a_tag.text.strip()
            logger.debug(f"Found on DDG: {title[:50]}...")
            results.append({
                "title": title,
                "url": a_tag.get("href"),
                "source": "DuckDuckGo",
                "image_url": None
            })
        return results

    def fetch_full_content(self, url):
        logger.info(f"Scraper: Extracting full content from {url}")
        try:
            res = requests.get(url, headers=self.headers, timeout=self.timeout, allow_redirects=True)
            soup = BeautifulSoup(res.text, "html.parser")
            paragraphs = soup.find_all("p")
            content = " ".join(p.text for p in paragraphs[:10])
            logger.info(f"Scraper: Extracted {len(content)} characters of text")
            return {"content": content.strip(), "url": res.url}
        except Exception as e:
            logger.error(f"Scraper: Failed to extract content: {e}")
            return {"content": "", "url": url}