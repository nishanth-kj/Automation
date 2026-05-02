import requests
import asyncio
from bs4 import BeautifulSoup
from utils.logger import logger
from repository.news_repository import NewsRepository
from utils.contants.status import Status
from utils.websocket_manager import manager

class NewsService:
    def __init__(self, timeout=10):
        self.timeout = timeout
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        self.news_repo = NewsRepository()

    async def run_background_scraper(self, query="trending", limit=20):
        """Handle the complete scraper lifecycle: Fetch -> Save -> Broadcast"""
        await manager.broadcast({"status": "starting", "message": f"Starting fetch for '{query}'"})
        
        # Scrape
        items = self.fetch_web(query=query, limit=limit)
        
        await manager.broadcast({"status": "saving", "message": f"Found {len(items)} items. Saving to DB..."})
        
        # Save as PENDING
        saved_ids = self.news_repo.save_all(items, status=Status.PENDING.code)
        
        # Broadcast pending items to UI
        pending_items = []
        for news_id in saved_ids:
            item = self.news_repo.get_by_id(news_id)
            if item:
                pending_items.append(item)
        
        await manager.broadcast({"status": "pending", "items": pending_items})
        
        # Move to ACTIVE
        self.news_repo.update_status(saved_ids, Status.ACTIVE.code)
        await manager.broadcast({"status": "complete", "message": "Refresh complete!"})

    def get_all(self, page=0, size=20, sort_by="newest", sort_order="desc"):
        return self.news_repo.get_all(page=page, size=size, sort_by=sort_by, sort_order=sort_order)

    def get_by_id(self, news_id):
        return self.news_repo.get_by_id(news_id)

    def delete(self, news_id):
        return self.news_repo.delete(news_id)

    def fetch_web(self, query="trending", limit=20):
        logger.info(f"Scraper: Starting global fetch for query: '{query}'")
        all_results = []
        
        # 1. Google News
        try:
            res = self.fetch_google(query, limit=5)
            all_results.extend(res)
        except Exception as e:
            logger.error(f"Scraper: Google News error: {e}")

        # 2. Reddit
        try:
            res = self.fetch_reddit(query, limit=5)
            all_results.extend(res)
        except Exception as e:
            logger.error(f"Scraper: Reddit error: {e}")

        # 3. Bing News
        try:
            res = self.fetch_bing(query, limit=5)
            all_results.extend(res)
        except Exception as e:
            logger.error(f"Scraper: Bing News error: {e}")

        # Remove duplicates by URL
        seen_urls = set()
        unique_results = []
        for res in all_results:
            url = res["url"]
            if url not in seen_urls:
                unique_results.append(res)
                seen_urls.add(url)
        
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
            raw_link = a_tag.get("href")
            full_link = "https://news.google.com" + raw_link[1:]
            img_tag = article.select_one("img")
            img_url = img_tag.get("src") if img_tag else None
            results.append({"title": title, "url": full_link, "source": "Google News", "image_url": img_url})
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
            results.append({"title": a_tag.text.strip(), "url": a_tag.get("href"), "source": "Bing News", "image_url": None})
        return results