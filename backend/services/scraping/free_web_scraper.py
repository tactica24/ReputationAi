"""
Cost-Free Web Scraper for Social Media & News
Monitors public content without expensive APIs

Cost: $0/month for code, $50-100/month for proxies (optional)
"""

import asyncio
import aiohttp
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
import re
import hashlib


@dataclass
class ScrapedContent:
    """Represents scraped public content"""
    source: str  # twitter, instagram, reddit, news
    url: str
    author: str
    content: str
    timestamp: datetime
    images: List[str]
    engagement: Dict[str, int]  # likes, shares, comments
    content_hash: str
    
    
class PublicContentScraper:
    """
    Scrapes public web content without using paid APIs
    
    Sources:
    - Twitter (via Nitter - free Twitter frontend)
    - Instagram (public profiles only)
    - Reddit (via PRAW free tier)
    - News (RSS feeds)
    - Blogs (RSS/HTML)
    """
    
    def __init__(self, proxies: Optional[List[str]] = None):
        self.proxies = proxies or []
        self.proxy_index = 0
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        ]
    
    def _get_next_proxy(self) -> Optional[str]:
        """Rotate through proxies to avoid rate limits"""
        if not self.proxies:
            return None
        proxy = self.proxies[self.proxy_index]
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return proxy
    
    def _hash_content(self, content: str) -> str:
        """Create unique hash for deduplication"""
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    async def scrape_twitter_nitter(
        self, 
        username: str,
        keywords: List[str]
    ) -> List[ScrapedContent]:
        """
        Scrape Twitter using Nitter (free Twitter frontend)
        
        Nitter instances (rotate if one is down):
        - nitter.net
        - nitter.it
        - nitter.unixfox.eu
        
        Cost: $0
        """
        results = []
        nitter_instances = [
            'https://nitter.net',
            'https://nitter.it', 
            'https://nitter.unixfox.eu'
        ]
        
        async with aiohttp.ClientSession() as session:
            for instance in nitter_instances:
                try:
                    # Search for keywords mentioning username
                    search_query = f'{username} {" OR ".join(keywords)}'
                    url = f'{instance}/search?q={search_query}'
                    
                    headers = {'User-Agent': self.user_agents[0]}
                    proxy = self._get_next_proxy()
                    
                    async with session.get(
                        url, 
                        headers=headers,
                        proxy=proxy,
                        timeout=10
                    ) as response:
                        if response.status == 200:
                            html = await response.text()
                            soup = BeautifulSoup(html, 'html.parser')
                            
                            # Parse tweets
                            tweets = soup.find_all('div', class_='timeline-item')
                            for tweet in tweets:
                                content_div = tweet.find('div', class_='tweet-content')
                                if not content_div:
                                    continue
                                
                                content_text = content_div.get_text(strip=True)
                                
                                # Extract metadata
                                author_elem = tweet.find('a', class_='username')
                                author = author_elem.get_text(strip=True) if author_elem else 'Unknown'
                                
                                tweet_link = tweet.find('a', class_='tweet-link')
                                tweet_url = f"{instance}{tweet_link['href']}" if tweet_link else url
                                
                                # Extract images
                                images = []
                                img_divs = tweet.find_all('div', class_='attachments')
                                for img_div in img_divs:
                                    img_tags = img_div.find_all('img')
                                    images.extend([img['src'] for img in img_tags if 'src' in img.attrs])
                                
                                # Extract engagement (if available)
                                stats_div = tweet.find('div', class_='tweet-stats')
                                engagement = {'likes': 0, 'retweets': 0, 'replies': 0}
                                if stats_div:
                                    likes_elem = stats_div.find('span', class_='icon-heart')
                                    if likes_elem:
                                        likes_text = likes_elem.parent.get_text(strip=True)
                                        engagement['likes'] = self._parse_number(likes_text)
                                
                                results.append(ScrapedContent(
                                    source='twitter',
                                    url=tweet_url,
                                    author=author,
                                    content=content_text,
                                    timestamp=datetime.now(),  # Parse from HTML in production
                                    images=images,
                                    engagement=engagement,
                                    content_hash=self._hash_content(content_text)
                                ))
                            
                            break  # Success, no need to try other instances
                
                except Exception as e:
                    print(f"Nitter instance {instance} failed: {e}")
                    continue
        
        return results
    
    async def scrape_reddit_praw(
        self,
        subreddits: List[str],
        keywords: List[str],
        time_filter: str = 'day'
    ) -> List[ScrapedContent]:
        """
        Scrape Reddit using PRAW (free tier)
        
        PRAW free tier: 60 requests/minute
        Cost: $0
        """
        import praw  # pip install praw
        
        results = []
        
        # Free Reddit API credentials (create at reddit.com/prefs/apps)
        reddit = praw.Reddit(
            client_id='YOUR_CLIENT_ID',  # Free from reddit.com
            client_secret='YOUR_CLIENT_SECRET',
            user_agent='ReputationMonitor/1.0'
        )
        
        for subreddit_name in subreddits:
            try:
                subreddit = reddit.subreddit(subreddit_name)
                
                # Search for keywords
                query = ' OR '.join(keywords)
                for submission in subreddit.search(query, time_filter=time_filter, limit=100):
                    results.append(ScrapedContent(
                        source='reddit',
                        url=f'https://reddit.com{submission.permalink}',
                        author=str(submission.author),
                        content=f"{submission.title}\n\n{submission.selftext}",
                        timestamp=datetime.fromtimestamp(submission.created_utc),
                        images=self._extract_reddit_images(submission),
                        engagement={
                            'upvotes': submission.score,
                            'comments': submission.num_comments
                        },
                        content_hash=self._hash_content(submission.title + submission.selftext)
                    ))
                    
                    # Also check comments
                    submission.comments.replace_more(limit=5)
                    for comment in submission.comments.list()[:50]:
                        if any(kw.lower() in comment.body.lower() for kw in keywords):
                            results.append(ScrapedContent(
                                source='reddit',
                                url=f'https://reddit.com{comment.permalink}',
                                author=str(comment.author),
                                content=comment.body,
                                timestamp=datetime.fromtimestamp(comment.created_utc),
                                images=[],
                                engagement={
                                    'upvotes': comment.score
                                },
                                content_hash=self._hash_content(comment.body)
                            ))
            
            except Exception as e:
                print(f"Reddit scraping error for r/{subreddit_name}: {e}")
                continue
        
        return results
    
    async def scrape_instagram_public(
        self,
        username: str
    ) -> List[ScrapedContent]:
        """
        Scrape Instagram public profiles using Instaloader
        
        Only public posts, no login required
        Cost: $0
        """
        from instaloader import Instaloader, Profile  # pip install instaloader
        
        results = []
        
        try:
            L = Instaloader()
            
            # Load profile
            profile = Profile.from_username(L.context, username)
            
            # Get recent posts (public only)
            for post in profile.get_posts():
                if post.is_video:
                    continue  # Skip videos for now
                
                results.append(ScrapedContent(
                    source='instagram',
                    url=f'https://instagram.com/p/{post.shortcode}',
                    author=username,
                    content=post.caption or '',
                    timestamp=post.date_utc,
                    images=[post.url],
                    engagement={
                        'likes': post.likes,
                        'comments': post.comments
                    },
                    content_hash=self._hash_content(post.caption or post.shortcode)
                ))
                
                # Limit to recent 50 posts
                if len(results) >= 50:
                    break
        
        except Exception as e:
            print(f"Instagram scraping error for @{username}: {e}")
        
        return results
    
    async def scrape_news_rss(
        self,
        keywords: List[str],
        sources: Optional[List[str]] = None
    ) -> List[ScrapedContent]:
        """
        Scrape news using free RSS feeds
        
        Free sources:
        - Google News RSS
        - Bing News RSS
        - NewsAPI.org free tier (100 requests/day)
        
        Cost: $0
        """
        import feedparser  # pip install feedparser
        
        results = []
        
        # Google News RSS (FREE, unlimited)
        for keyword in keywords:
            google_news_url = f'https://news.google.com/rss/search?q={keyword}'
            
            try:
                feed = feedparser.parse(google_news_url)
                
                for entry in feed.entries[:20]:  # Limit per keyword
                    results.append(ScrapedContent(
                        source='google_news',
                        url=entry.link,
                        author=entry.get('source', {}).get('title', 'Unknown'),
                        content=f"{entry.title}\n\n{entry.get('summary', '')}",
                        timestamp=datetime(*entry.published_parsed[:6]) if hasattr(entry, 'published_parsed') else datetime.now(),
                        images=[],
                        engagement={},
                        content_hash=self._hash_content(entry.title)
                    ))
            
            except Exception as e:
                print(f"Google News RSS error for '{keyword}': {e}")
        
        return results
    
    async def scrape_news_api_free(
        self,
        keywords: List[str]
    ) -> List[ScrapedContent]:
        """
        Scrape using NewsAPI.org free tier
        
        Free tier: 100 requests/day (3,000/month)
        Cost: $0
        """
        results = []
        
        # NewsAPI.org free API key (get from newsapi.org)
        API_KEY = 'YOUR_FREE_API_KEY'
        
        async with aiohttp.ClientSession() as session:
            for keyword in keywords:
                url = f'https://newsapi.org/v2/everything?q={keyword}&apiKey={API_KEY}&pageSize=20'
                
                try:
                    async with session.get(url) as response:
                        if response.status == 200:
                            data = await response.json()
                            
                            for article in data.get('articles', []):
                                results.append(ScrapedContent(
                                    source='newsapi',
                                    url=article['url'],
                                    author=article.get('author', 'Unknown'),
                                    content=f"{article['title']}\n\n{article.get('description', '')}",
                                    timestamp=datetime.fromisoformat(article['publishedAt'].replace('Z', '+00:00')),
                                    images=[article['urlToImage']] if article.get('urlToImage') else [],
                                    engagement={},
                                    content_hash=self._hash_content(article['title'])
                                ))
                
                except Exception as e:
                    print(f"NewsAPI error for '{keyword}': {e}")
        
        return results
    
    async def scrape_tiktok_public(
        self,
        username: str
    ) -> List[ScrapedContent]:
        """
        Scrape TikTok public videos
        
        Using TikTok-Api (free, no official API needed)
        Cost: $0
        """
        from TikTokApi import TikTokApi  # pip install TikTokApi
        
        results = []
        
        try:
            async with TikTokApi() as api:
                user = api.user(username)
                
                async for video in user.videos(count=30):
                    video_data = await video.info()
                    
                    results.append(ScrapedContent(
                        source='tiktok',
                        url=f'https://tiktok.com/@{username}/video/{video_data["id"]}',
                        author=username,
                        content=video_data.get('desc', ''),
                        timestamp=datetime.fromtimestamp(video_data.get('createTime', 0)),
                        images=[video_data.get('video', {}).get('cover', '')],
                        engagement={
                            'likes': video_data.get('stats', {}).get('diggCount', 0),
                            'comments': video_data.get('stats', {}).get('commentCount', 0),
                            'shares': video_data.get('stats', {}).get('shareCount', 0)
                        },
                        content_hash=self._hash_content(video_data.get('desc', ''))
                    ))
        
        except Exception as e:
            print(f"TikTok scraping error for @{username}: {e}")
        
        return results
    
    def _parse_number(self, text: str) -> int:
        """Parse engagement numbers (e.g., '1.2K' -> 1200)"""
        text = text.strip().upper()
        multipliers = {'K': 1000, 'M': 1000000, 'B': 1000000000}
        
        for suffix, multiplier in multipliers.items():
            if suffix in text:
                try:
                    num = float(text.replace(suffix, '').strip())
                    return int(num * multiplier)
                except:
                    pass
        
        try:
            return int(''.join(filter(str.isdigit, text)))
        except:
            return 0
    
    def _extract_reddit_images(self, submission) -> List[str]:
        """Extract images from Reddit submission"""
        images = []
        
        if hasattr(submission, 'url') and any(
            ext in submission.url.lower() 
            for ext in ['.jpg', '.jpeg', '.png', '.gif']
        ):
            images.append(submission.url)
        
        if hasattr(submission, 'preview'):
            try:
                preview_images = submission.preview['images']
                for img in preview_images:
                    if 'source' in img:
                        images.append(img['source']['url'])
            except:
                pass
        
        return images


class MonitoringOrchestrator:
    """
    Orchestrates all scraping activities
    Runs on schedule (cron-like)
    """
    
    def __init__(self, scraper: PublicContentScraper):
        self.scraper = scraper
    
    async def monitor_person(
        self,
        person_name: str,
        aliases: List[str],
        social_handles: Dict[str, str],  # {platform: username}
        keywords: List[str]
    ) -> List[ScrapedContent]:
        """
        Complete monitoring sweep for one person
        """
        all_results = []
        
        # Combine person name with aliases for search
        search_terms = [person_name] + aliases + keywords
        
        # Twitter monitoring
        if 'twitter' in social_handles:
            twitter_results = await self.scraper.scrape_twitter_nitter(
                social_handles['twitter'],
                search_terms
            )
            all_results.extend(twitter_results)
            print(f"✅ Twitter: Found {len(twitter_results)} mentions")
        
        # Reddit monitoring
        reddit_results = await self.scraper.scrape_reddit_praw(
            subreddits=['all', 'news', 'worldnews'],
            keywords=search_terms
        )
        all_results.extend(reddit_results)
        print(f"✅ Reddit: Found {len(reddit_results)} mentions")
        
        # Instagram monitoring
        if 'instagram' in social_handles:
            instagram_results = await self.scraper.scrape_instagram_public(
                social_handles['instagram']
            )
            all_results.extend(instagram_results)
            print(f"✅ Instagram: Found {len(instagram_results)} posts")
        
        # News monitoring
        news_results = await self.scraper.scrape_news_rss(search_terms)
        all_results.extend(news_results)
        print(f"✅ Google News: Found {len(news_results)} articles")
        
        # NewsAPI (free tier)
        newsapi_results = await self.scraper.scrape_news_api_free(search_terms)
        all_results.extend(newsapi_results)
        print(f"✅ NewsAPI: Found {len(newsapi_results)} articles")
        
        # TikTok monitoring
        if 'tiktok' in social_handles:
            tiktok_results = await self.scraper.scrape_tiktok_public(
                social_handles['tiktok']
            )
            all_results.extend(tiktok_results)
            print(f"✅ TikTok: Found {len(tiktok_results)} videos")
        
        # Deduplicate by content hash
        unique_results = self._deduplicate(all_results)
        
        print(f"\n📊 Total unique mentions: {len(unique_results)}")
        
        return unique_results
    
    def _deduplicate(self, results: List[ScrapedContent]) -> List[ScrapedContent]:
        """Remove duplicate content based on hash"""
        seen_hashes = set()
        unique = []
        
        for result in results:
            if result.content_hash not in seen_hashes:
                seen_hashes.add(result.content_hash)
                unique.append(result)
        
        return unique


# Example usage
async def main():
    """
    Example: Monitor a public figure
    """
    # Optional: Use rotating proxies for better reliability
    # proxies = ['http://proxy1:port', 'http://proxy2:port']
    proxies = None  # Start without proxies (free)
    
    scraper = PublicContentScraper(proxies=proxies)
    orchestrator = MonitoringOrchestrator(scraper)
    
    # Monitor example person
    results = await orchestrator.monitor_person(
        person_name="John Doe",
        aliases=["J. Doe", "John D"],
        social_handles={
            'twitter': 'johndoe',
            'instagram': 'johndoe',
            'tiktok': 'johndoe'
        },
        keywords=["scam", "fraud", "fake", "deepfake", "controversy"]
    )
    
    # Filter for potential threats
    threats = [
        r for r in results 
        if any(
            word in r.content.lower() 
            for word in ['scam', 'fraud', 'fake', 'deepfake', 'lies']
        )
    ]
    
    print(f"\n🚨 Potential threats detected: {len(threats)}")
    for threat in threats[:5]:
        print(f"  - {threat.source}: {threat.content[:100]}...")
        print(f"    URL: {threat.url}\n")


if __name__ == "__main__":
    asyncio.run(main())
