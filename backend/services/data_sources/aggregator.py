"""
Data Source Aggregator
Multi-source data collection from social media APIs, news, blogs, forums, reviews
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
from abc import ABC, abstractmethod
import asyncio


@dataclass
class Mention:
    """Standardized mention data structure"""
    id: str
    entity_id: str
    text: str
    source: str
    source_url: str
    author: str
    author_url: Optional[str]
    timestamp: datetime
    engagement: Dict[str, int]  # likes, shares, comments
    metadata: Dict[str, Any]
    raw_data: Dict[str, Any]
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "entity_id": self.entity_id,
            "text": self.text,
            "source": self.source,
            "source_url": self.source_url,
            "author": self.author,
            "author_url": self.author_url,
            "timestamp": self.timestamp.isoformat(),
            "likes": self.engagement.get('likes', 0),
            "shares": self.engagement.get('shares', 0),
            "comments": self.engagement.get('comments', 0),
            "metadata": self.metadata
        }


class DataSource(ABC):
    """Abstract base class for data sources"""
    
    def __init__(self, api_key: Optional[str] = None, config: Optional[Dict] = None):
        self.api_key = api_key
        self.config = config or {}
        self.rate_limit_remaining = 1000
        self.last_request_time = None
    
    @abstractmethod
    async def fetch_mentions(
        self, 
        entity: str, 
        since: datetime,
        max_results: int = 100
    ) -> List[Mention]:
        """Fetch mentions for an entity"""
        pass
    
    @abstractmethod
    def validate_credentials(self) -> bool:
        """Validate API credentials"""
        pass
    
    def _check_rate_limit(self):
        """Check and enforce rate limiting"""
        if self.rate_limit_remaining <= 0:
            raise Exception("Rate limit exceeded")
        self.rate_limit_remaining -= 1


class TwitterSource(DataSource):
    """Twitter/X API integration"""
    
    async def fetch_mentions(
        self,
        entity: str,
        since: datetime,
        max_results: int = 100
    ) -> List[Mention]:
        """
        Fetch mentions from Twitter/X
        
        Args:
            entity: Entity to search for
            since: Start datetime
            max_results: Maximum results to return
            
        Returns:
            List of Mention objects
        """
        self._check_rate_limit()
        
        # Placeholder for actual Twitter API integration
        # In production: Use tweepy or httpx to call Twitter API v2
        
        mentions = []
        
        # Simulated API call
        # In production: Replace with actual API call
        """
        import tweepy
        
        client = tweepy.Client(bearer_token=self.api_key)
        tweets = client.search_recent_tweets(
            query=f'"{entity}"',
            max_results=max_results,
            start_time=since,
            tweet_fields=['created_at', 'public_metrics', 'author_id']
        )
        
        for tweet in tweets.data:
            mention = Mention(
                id=f"twitter_{tweet.id}",
                entity_id=entity,
                text=tweet.text,
                source="twitter",
                source_url=f"https://twitter.com/i/status/{tweet.id}",
                author=tweet.author_id,
                author_url=f"https://twitter.com/user/{tweet.author_id}",
                timestamp=tweet.created_at,
                engagement={
                    'likes': tweet.public_metrics['like_count'],
                    'shares': tweet.public_metrics['retweet_count'],
                    'comments': tweet.public_metrics['reply_count']
                },
                metadata={'tweet_id': tweet.id},
                raw_data=tweet.data
            )
            mentions.append(mention)
        """
        
        return mentions
    
    def validate_credentials(self) -> bool:
        """Validate Twitter API credentials"""
        if not self.api_key:
            return False
        # In production: Test API call
        return True


class LinkedInSource(DataSource):
    """LinkedIn API integration"""
    
    async def fetch_mentions(
        self,
        entity: str,
        since: datetime,
        max_results: int = 100
    ) -> List[Mention]:
        """Fetch mentions from LinkedIn"""
        self._check_rate_limit()
        
        # Placeholder for LinkedIn API integration
        # Note: LinkedIn API has restricted access
        mentions = []
        return mentions
    
    def validate_credentials(self) -> bool:
        """Validate LinkedIn API credentials"""
        return bool(self.api_key)


class NewsAPISource(DataSource):
    """News API integration for media monitoring"""
    
    async def fetch_mentions(
        self,
        entity: str,
        since: datetime,
        max_results: int = 100
    ) -> List[Mention]:
        """
        Fetch news articles mentioning entity
        
        Uses NewsAPI.org or similar service
        """
        self._check_rate_limit()
        
        mentions = []
        
        # Placeholder for News API integration
        """
        from newsapi import NewsApiClient
        
        newsapi = NewsApiClient(api_key=self.api_key)
        
        articles = newsapi.get_everything(
            q=entity,
            from_param=since.isoformat(),
            language='en',
            sort_by='publishedAt',
            page_size=max_results
        )
        
        for article in articles['articles']:
            mention = Mention(
                id=f"news_{hash(article['url'])}",
                entity_id=entity,
                text=article['title'] + " " + article['description'],
                source="news",
                source_url=article['url'],
                author=article['source']['name'],
                author_url=article['source'].get('url'),
                timestamp=datetime.fromisoformat(article['publishedAt']),
                engagement={'likes': 0, 'shares': 0, 'comments': 0},
                metadata={
                    'source_name': article['source']['name'],
                    'image': article.get('urlToImage')
                },
                raw_data=article
            )
            mentions.append(mention)
        """
        
        return mentions
    
    def validate_credentials(self) -> bool:
        """Validate News API credentials"""
        return bool(self.api_key)


class RedditSource(DataSource):
    """Reddit API integration"""
    
    async def fetch_mentions(
        self,
        entity: str,
        since: datetime,
        max_results: int = 100
    ) -> List[Mention]:
        """Fetch mentions from Reddit"""
        self._check_rate_limit()
        
        mentions = []
        
        # Placeholder for Reddit API (PRAW) integration
        """
        import praw
        
        reddit = praw.Reddit(
            client_id=self.config.get('client_id'),
            client_secret=self.config.get('client_secret'),
            user_agent=self.config.get('user_agent')
        )
        
        # Search across all subreddits
        for submission in reddit.subreddit('all').search(entity, limit=max_results):
            if submission.created_utc >= since.timestamp():
                mention = Mention(
                    id=f"reddit_{submission.id}",
                    entity_id=entity,
                    text=submission.title + " " + submission.selftext,
                    source="reddit",
                    source_url=f"https://reddit.com{submission.permalink}",
                    author=str(submission.author),
                    author_url=f"https://reddit.com/u/{submission.author}",
                    timestamp=datetime.fromtimestamp(submission.created_utc),
                    engagement={
                        'likes': submission.score,
                        'shares': 0,
                        'comments': submission.num_comments
                    },
                    metadata={
                        'subreddit': submission.subreddit.display_name,
                        'upvote_ratio': submission.upvote_ratio
                    },
                    raw_data=vars(submission)
                )
                mentions.append(mention)
        """
        
        return mentions
    
    def validate_credentials(self) -> bool:
        """Validate Reddit API credentials"""
        required = ['client_id', 'client_secret', 'user_agent']
        return all(key in self.config for key in required)


class ReviewSiteSource(DataSource):
    """Integration for review sites (Trustpilot, Yelp, Google Reviews, etc.)"""
    
    async def fetch_mentions(
        self,
        entity: str,
        since: datetime,
        max_results: int = 100
    ) -> List[Mention]:
        """Fetch reviews for entity"""
        self._check_rate_limit()
        
        mentions = []
        # Placeholder - would integrate with specific review site APIs
        return mentions
    
    def validate_credentials(self) -> bool:
        """Validate review site API credentials"""
        return bool(self.api_key)


class WebScraperSource(DataSource):
    """
    Custom web scraper for sources without public APIs
    GDPR/NDPR compliant scraping
    """
    
    async def fetch_mentions(
        self,
        entity: str,
        since: datetime,
        max_results: int = 100
    ) -> List[Mention]:
        """
        Scrape web sources for mentions
        
        Uses: BeautifulSoup, Scrapy, or Playwright for dynamic content
        """
        mentions = []
        
        # Placeholder for web scraping logic
        """
        from bs4 import BeautifulSoup
        import httpx
        
        # Define target URLs to scrape
        target_urls = self.config.get('target_urls', [])
        
        async with httpx.AsyncClient() as client:
            for url in target_urls:
                try:
                    # Respect robots.txt
                    if not self._check_robots_txt(url):
                        continue
                    
                    response = await client.get(url, timeout=10.0)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Extract content (site-specific logic)
                    articles = soup.find_all('article')
                    
                    for article in articles:
                        if entity.lower() in article.text.lower():
                            # Extract and create mention
                            pass
                            
                except Exception as e:
                    print(f"Error scraping {url}: {e}")
        """
        
        return mentions
    
    def validate_credentials(self) -> bool:
        """No credentials needed for scraping"""
        return True
    
    def _check_robots_txt(self, url: str) -> bool:
        """Check if scraping is allowed by robots.txt"""
        # Placeholder for robots.txt checking
        return True


class DataAggregator:
    """
    Aggregates data from multiple sources
    Manages rate limiting, deduplication, and data normalization
    """
    
    def __init__(self):
        self.sources: Dict[str, DataSource] = {}
        self.mention_cache: List[Mention] = []
    
    def add_source(self, name: str, source: DataSource):
        """Add a data source to the aggregator"""
        if source.validate_credentials():
            self.sources[name] = source
        else:
            raise ValueError(f"Invalid credentials for source: {name}")
    
    async def fetch_all_mentions(
        self,
        entity: str,
        entity_id: str,
        since: datetime,
        sources: Optional[List[str]] = None
    ) -> List[Mention]:
        """
        Fetch mentions from all configured sources
        
        Args:
            entity: Entity name to search for
            entity_id: Unique entity identifier
            since: Fetch mentions since this time
            sources: Optional list of specific sources to use
            
        Returns:
            Deduplicated list of mentions
        """
        if sources is None:
            sources = list(self.sources.keys())
        
        # Fetch from all sources concurrently
        tasks = []
        for source_name in sources:
            if source_name in self.sources:
                task = self.sources[source_name].fetch_mentions(
                    entity=entity,
                    since=since,
                    max_results=100
                )
                tasks.append(task)
        
        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Flatten results and handle errors
        all_mentions = []
        for result in results:
            if isinstance(result, list):
                all_mentions.extend(result)
            elif isinstance(result, Exception):
                print(f"Error fetching from source: {result}")
        
        # Deduplicate mentions
        unique_mentions = self._deduplicate_mentions(all_mentions)
        
        # Cache mentions
        self.mention_cache.extend(unique_mentions)
        
        return unique_mentions
    
    def _deduplicate_mentions(self, mentions: List[Mention]) -> List[Mention]:
        """
        Remove duplicate mentions based on text similarity and timestamp
        """
        seen = set()
        unique = []
        
        for mention in mentions:
            # Create hash based on text and timestamp
            key = (
                mention.text[:100].lower().strip(),
                mention.timestamp.date(),
                mention.source
            )
            
            if key not in seen:
                seen.add(key)
                unique.append(mention)
        
        return unique
    
    def get_source_statistics(self) -> Dict:
        """Get statistics about data sources"""
        stats = {
            "total_sources": len(self.sources),
            "active_sources": [],
            "total_mentions_cached": len(self.mention_cache)
        }
        
        for name, source in self.sources.items():
            stats["active_sources"].append({
                "name": name,
                "rate_limit_remaining": source.rate_limit_remaining
            })
        
        return stats


# Example usage
if __name__ == "__main__":
    async def main():
        # Initialize aggregator
        aggregator = DataAggregator()
        
        # Add sources (with dummy credentials for demo)
        try:
            aggregator.add_source("twitter", TwitterSource(api_key="dummy_key"))
            aggregator.add_source("news", NewsAPISource(api_key="dummy_key"))
            aggregator.add_source("reddit", RedditSource(config={
                'client_id': 'dummy',
                'client_secret': 'dummy',
                'user_agent': 'ReputationAI v1.0'
            }))
        except ValueError as e:
            print(f"Source configuration error: {e}")
        
        # Fetch mentions
        since = datetime.now() - timedelta(days=7)
        mentions = await aggregator.fetch_all_mentions(
            entity="Example Company",
            entity_id="company_123",
            since=since
        )
        
        print(f"\nFetched {len(mentions)} mentions")
        print(f"Sources: {aggregator.get_source_statistics()}")
    
    # Run async main
    from datetime import timedelta
    asyncio.run(main())
