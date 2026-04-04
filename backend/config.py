"""
Kronaxis — Centralized Configuration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
All settings, constants, and sector keyword maps.
Covers ALL global sectors: finance, tech, health, science, politics,
sports, entertainment, defense, environment, law, education, space,
fashion, food, energy, transport, agriculture, and more.
"""

import os
import random
import uuid
from pathlib import Path
from dotenv import load_dotenv  # type: ignore
from datetime import datetime, timedelta

# ── Load .env from project root ──────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent.resolve()
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
load_dotenv(BASE_DIR / ".env")

DB_PATH = DATA_DIR / "intelligence.db"

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/Kronaxis")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# ── API Keys & Credentials ─────────────────────────────────────────────────────────────────
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "797934e03b33474cb8685d392f0b5335")
NEWSDATA_API_KEY = os.getenv("NEWSDATA_API_KEY", "pub_c97f479240b7412e9ec56bf9acc953b5")
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY", "ad0fdcffbdce1cacf14b18dd44260112")
WORLDNEWS_API_KEY = os.getenv("WORLDNEWS_API_KEY", "a0079caa91044730bcb54dcbbcf6dea5")
WEBZ_API_KEY = os.getenv("WEBZ_API_KEY", "4a6b0b05-34cf-475e-8a77-2de06c3f4750")
GDELT_API_URL = "https://api.gdeltproject.org/api/v2/doc/doc?query=news&mode=ArtList&maxrecords=100&format=json"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyB3iLyylOu0tLrWbGJqYyeGMcsHtiVCNTk")

# ── Hugging Face API Token (for large model inference) ────────────────────────
HF_API_TOKEN = os.getenv("HF_API_TOKEN", "")

# ── Sector-Specific AI Model IDs ─────────────────────────────────────────────
SECTOR_MODELS = {
    "finance":    "ProsusAI/finbert",
    "technology": "Qwen/Qwen2-7B-Instruct",
    "politics":   "mistralai/Mistral-7B-Instruct-v0.3",
    "business":   "deepseek-ai/deepseek-llm-7b-chat",
    "health":     "microsoft/BioGPT-Large",
    "general":    "meta-llama/Llama-3-8B-Instruct",
}

# ── Core NLP Model IDs ──────────────────────────────────────────────────────
SENTIMENT_MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
NER_MODEL = "en_core_web_sm"  # spaCy model

# ── Collection Settings ──────────────────────────────────────────────────────
FETCH_INTERVAL_SECONDS = 180
MAX_ARTICLES_PER_FETCH = 50
NEWS_CATEGORIES = ["general", "technology", "business", "science", "health", "sports", "entertainment"]
NEWS_COUNTRY = "us"

# ── RSS Feed URLs (free, unlimited, global multi-domain) ─────────────────────
# Note: optimized for reliability and speed (removed slow feeds)
RSS_FEEDS = [
    # ── Global & World Events (Massive Coverage) ──
    "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en",
    "https://feeds.bbci.co.uk/news/rss.xml",
    "https://feeds.bbci.co.uk/news/world/rss.xml",
    "http://rss.cnn.com/rss/edition.rss",
    "http://rss.cnn.com/rss/edition_world.rss",
    "https://www.aljazeera.com/xml/rss/all.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "https://www.reutersagency.com/feed/?best-topics=political-general&type=rx",
    "https://feeds.npr.org/1001/rss.xml",
    "https://news.google.com/rss/search?q=reuters&hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss/search?q=asia+news&hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss/search?q=africa+news&hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss/search?q=middle+east+news&hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss/search?q=latin+america+news&hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss/search?q=europe+news&hl=en-GB&gl=GB&ceid=GB:en",
    "https://www.theguardian.com/world/rss",
    "https://www.theguardian.com/international/rss",
    "https://feeds.foxnews.com/foxnews/world",

    # ── India National News (High Volume) ──
    "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en",
    "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
    "https://timesofindia.indiatimes.com/rssfeeds/296589292.cms",
    "https://www.thehindu.com/news/national/feeder/default.rss",
    "https://feeds.feedburner.com/ndtvnews-top-stories",
    "https://www.news18.com/rss/india.xml",
    "https://zeenews.india.com/rss/india-national-news.xml",
    "https://indianexpress.com/feed/",
    "https://www.livemint.com/rss/news",

    # ── Tamil Nadu & Regional News (Specifically Requested) ──
    "https://news.google.com/rss/search?q=tamil+nadu&hl=en-IN&gl=IN&ceid=IN:en",
    "https://news.google.com/rss/search?q=chennai&hl=en-IN&gl=IN&ceid=IN:en",
    "https://timesofindia.indiatimes.com/rssfeeds/2950623.cms", # Chennai TOI
    "https://www.thehindu.com/news/national/tamil-nadu/feeder/default.rss", # Hindu TN
    "https://www.thehindu.com/news/cities/chennai/feeder/default.rss", # Hindu Chennai
    "https://www.news18.com/rss/tamil-nadu.xml",
    "https://tamil.oneindia.com/rss/tamil-news-fb.xml", # OneIndia Tamil
    "https://feeds.bbci.co.uk/tamil/rss.xml", # BBC Tamil
    "https://news.google.com/rss/search?q=tamil+news&hl=en-IN&gl=IN&ceid=IN:en",

    # ── Science & Technology ──
    "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
    "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    "https://www.theverge.com/rss/index.xml",
    "https://www.wired.com/feed/rss",
    "https://techcrunch.com/feed/",
    "https://rss.sciencedaily.com/top/science_news.xml",

    # ── Business & Economy ──
    "https://feeds.bbci.co.uk/news/business/rss.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml",
    "https://www.livemint.com/rss/markets",
    "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
    "https://home.treasury.gov/news/press-releases/rss.xml",
    "https://finance.yahoo.com/news/rssindex",

    # ── Sports (comprehensive) ──
    "https://feeds.bbci.co.uk/sport/rss.xml",
    "https://www.espn.com/espn/rss/news",
    "https://timesofindia.indiatimes.com/rssfeeds/4719148.cms", # TOI Sports India
    "https://www.thehindu.com/sport/feeder/default.rss",
    "https://sports.yahoo.com/rss/",

    # ── Health, Entertainment & Politics ──
    "https://feeds.bbci.co.uk/news/health/rss.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/Health.xml",
    "https://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml",
    "https://feeds.bbci.co.uk/news/politics/rss.xml",
    "https://www.thehindu.com/entertainment/feeder/default.rss",
    "https://variety.com/feed/",
]

# ── Artificial Intelligence Models \u0026 Clustering ─────────────────────────────
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
HDBSCAN_MIN_CLUSTER_SIZE = 2
HDBSCAN_MIN_SAMPLES = 1

# ── Source Credibility Database ──────────────────────────────────────────────
SOURCE_CREDIBILITY = {
    "reuters": 0.95,
    "bbc": 0.90,
    "bbci": 0.90,
    "bloomberg": 0.92,
    "nytimes": 0.94,
    "aljazeera": 0.88,
    "google": 0.85
}
DEFAULT_CREDIBILITY = 0.30

# ── Sentiment Thresholds ─────────────────────────────────────────────────────
POSITIVE_THRESHOLD = 0.05
NEGATIVE_THRESHOLD = -0.05

# ── Massive Global Sector Generator (3000+ Sectors across ALL fields) ────────
BASE_SECTORS = [
    # Finance & Economy
    "Finance", "Banking", "Insurance", "Cryptocurrency", "Venture Capital",
    # Technology
    "Technology", "Cybersecurity", "Artificial Intelligence", "Cloud Computing", "Semiconductors",
    # Healthcare & Biotech
    "Healthcare", "Pharmaceuticals", "Biotech", "Mental Health", "Medical Devices",
    # Energy & Environment
    "Energy", "Renewable Energy", "Oil & Gas", "Nuclear", "Climate",
    # Politics & Governance
    "Politics", "Diplomacy", "Defense", "Intelligence", "Law & Justice",
    # Transport & Logistics
    "Transport", "Aviation", "Shipping", "Automotive", "Railways",
    # Retail & Consumer
    "Retail", "E-Commerce", "Consumer Goods", "Luxury", "Food & Beverage",
    # Science & Research
    "Science", "Space", "Physics", "Astronomy", "Marine Biology",
    # Education
    "Education", "Higher Education", "EdTech", "Research", "Scholarships",
    # Entertainment & Media
    "Entertainment", "Film", "Music", "Gaming", "Streaming",
    # Sports
    "Sports", "Football", "Cricket", "Basketball", "Olympics",
    # Agriculture & Food
    "Agriculture", "Farming", "Fisheries", "Food Processing", "Organic",
    # Real Estate & Construction
    "Real Estate", "Construction", "Architecture", "Urban Planning", "Housing",
    # Manufacturing & Industry
    "Manufacturing", "Robotics", "Automation", "Textiles", "Steel",
    # Telecom & Media
    "Telecommunications", "Broadcasting", "Publishing", "Social Media", "Advertising",
    # Environment & Sustainability
    "Environment", "Wildlife", "Conservation", "Water Resources", "Forestry",
    # Arts & Culture
    "Arts", "Fashion", "Design", "Literature", "Heritage",
    # Aerospace & Defense
    "Aerospace", "Satellites", "Drones", "Military", "Naval",
    # Mining & Resources
    "Mining", "Rare Earth", "Gold", "Diamond", "Lithium",
    # Legal & Compliance
    "Legal", "Compliance", "Human Rights", "Immigration", "Trade Law",
]

MODIFIERS = [
    "Global", "Regional", "Advanced", "Consumer", "Enterprise", "Sustainable",
    "Quantum", "Digital", "Smart", "Green", "Urban", "Rural", "Nano", "Micro",
    "Macro", "Next-Gen", "Cloud", "Applied", "Theoretical", "Industrial",
    "Emerging", "International", "Domestic", "Strategic", "Tactical",
    "Decentralized", "Continental", "Arctic", "Tropical", "Precision",
]

SUB_CATEGORIES = [
    "Systems", "Services", "Infrastructure", "Analytics", "Operations",
    "Research", "Development", "Logistics", "Networks", "Solutions",
    "Markets", "Equities", "Assets", "Compliance", "Security",
    "Design", "Automation", "Synergy", "Ventures", "Holdings",
    "Policy", "Governance", "Innovation", "Strategy", "Intelligence",
    "Education", "Media", "Culture", "Production", "Distribution",
]

KEYWORDS_POOL = [
    # Finance
    "stock", "market", "bank", "investment", "trading", "economy", "gdp", "inflation", "interest rate", "bonds",
    # Technology
    "ai", "artificial intelligence", "machine learning", "software", "hardware", "startup", "data", "cyber",
    "robotics", "automation", "quantum", "blockchain", "cloud", "saas", "5g",
    # Healthcare
    "healthcare", "medical", "hospital", "vaccine", "drug", "pharma", "clinical", "patient", "surgery", "disease",
    # Energy
    "oil", "gas", "solar", "wind", "renewable", "energy", "nuclear", "electricity", "power grid", "carbon",
    # Politics
    "election", "president", "government", "policy", "congress", "parliament", "vote", "diplomat", "sanction", "treaty",
    # Transport
    "airline", "shipping", "logistics", "freight", "railroad", "supply chain", "aviation", "transport", "ev", "electric vehicle",
    # Sports
    "football", "soccer", "cricket", "basketball", "tennis", "olympics", "world cup", "championship", "athlete", "tournament",
    # Entertainment
    "movie", "film", "music", "concert", "streaming", "netflix", "gaming", "esports", "celebrity", "album",
    # Science
    "research", "discovery", "space", "nasa", "satellite", "experiment", "physics", "biology", "chemistry", "astronomy",
    # Environment
    "climate", "environment", "pollution", "wildlife", "forest", "ocean", "sustainability", "emissions", "recycling", "biodiversity",
    # Education
    "university", "school", "education", "student", "scholarship", "degree", "learning", "academic", "professor", "curriculum",
    # Food & Agriculture
    "agriculture", "farming", "crop", "harvest", "food", "nutrition", "organic", "livestock", "fisheries", "grain",
    # Retail
    "retail", "consumer", "shopping", "e-commerce", "amazon", "walmart", "brand", "sales", "revenue", "profit",
    # Real Estate
    "real estate", "property", "housing", "construction", "mortgage", "rent", "building", "architecture", "zoning", "development",
    # Defense
    "defense", "military", "army", "navy", "air force", "missile", "weapon", "security", "intelligence", "surveillance",
    # Legal
    "court", "law", "legal", "judge", "lawsuit", "regulation", "compliance", "rights", "crime", "justice",
    # Fashion & Arts
    "fashion", "design", "art", "gallery", "museum", "exhibition", "luxury", "brand", "model", "couture",
    # Mining
    "mining", "gold", "diamond", "lithium", "cobalt", "rare earth", "extraction", "mineral", "ore", "geological",
]


def generate_sectors(count=3000):
    sectors = {}
    for i in range(count):
        base = random.choice(BASE_SECTORS)
        mod = random.choice(MODIFIERS)
        sub = random.choice(SUB_CATEGORIES)
        sector_name = f"{mod} {base} {sub} {i}"

        # Give random keywords for matching
        kw = random.sample(KEYWORDS_POOL, k=random.randint(2, 6))
        # Add exact match parts
        kw.extend([base.lower(), mod.lower(), sub.lower()])
        sectors[sector_name] = kw
    return sectors


print("Generating 3000 Global Sectors (all fields)...")
SECTOR_KEYWORDS = generate_sectors(3000)

# ── Massive Article Dataset Generator (sample data for offline mode) ──────────
SOURCES = [
    "NewsData.io", "World News API", "GDELT Network", "RSS Feed Matrix",
    "GNews Intelligence", "Webz.io Analytics", "NewsAPI Cluster",
    "Reuters", "Bloomberg", "TechCrunch", "Wired", "BBC News", "CNBC",
    "Financial Times", "The Verge", "Guardian", "Nature", "MarketWatch",
    "AP News", "ESPN", "Sky Sports", "Variety", "Rolling Stone",
    "Scientific American", "National Geographic", "Vogue", "Forbes"
]
ACTIONS = [
    "Surges", "Plummets", "Hits Record", "Announces", "Expands",
    "Faces Scrutiny Over", "Unveils", "Acquires", "Merges With",
    "Discovers", "Releases", "Halts", "Invests in", "Predicts",
    "Launches", "Suspends", "Investigates", "Celebrates", "Wins", "Signs",
    "Secures Victory Against", "Breaks World Record In", "Suffers Defeat In",
    "Announces New Manager For"
]
SUBJECTS = [
    "AI Models", "Global Markets", "Oil Prices", "Crypto Assets",
    "Healthcare Startups", "Tech Giants", "Federal Reserve", "Supply Chains",
    "Semiconductor Production", "Renewable Energy Networks", "Electric Vehicles",
    "Quantum Computing", "Space Logistics", "Retail Consumption",
    "Olympic Committee", "Film Industry", "Climate Scientists",
    "Military Operations", "Education Reform", "Fashion Week",
    "Agricultural Output", "Mining Operations", "Streaming Platforms",
    "World Cup Organizers", "University Rankings", "Wildlife Conservation",
    "Premier League Clubs", "Formula 1 Teams", "Tennis Grand Slams",
    "NBA Franchises", "NFL Super Bowl", "Champions League"
]


def generate_sample_data(count=50):
    articles = []
    base_time = datetime.utcnow()
    for i in range(count):
        subj = random.choice(SUBJECTS)
        act = random.choice(ACTIONS)
        base = random.choice(BASE_SECTORS)
        title = f"{subj} {act} New {base} Initiative {i}"

        articles.append({
            "title": title,
            "description": f"In a surprising turn of events, {subj.lower()} {act.lower()} operations related to {base.lower()}, impacting global developments significantly. " + " ".join(random.sample(KEYWORDS_POOL, 5)),
            "source": random.choice(SOURCES),
            "url": f"https://example.com/article/{str(uuid.uuid4().hex)[:8]}",
            "published_at": (base_time - timedelta(minutes=random.randint(1, 10000))).isoformat() + "Z"
        })
    return articles


print("Generating 50 Sample Articles (global coverage)...")
SAMPLE_ARTICLES = generate_sample_data(50)
