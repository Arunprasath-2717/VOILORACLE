"""
VEILORACLE — Region Intelligence Engine
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Detects location automatically and classifies articles into regions strictly:
Tamil Nadu > India > World.
"""

import logging
import re

logger = logging.getLogger("veiloracle.classifier")

TN_KEYWORDS = {
    # Core
    "tamil nadu", "tn", "tamilnadu", "tamil nadu government", "tamil nadu news", 
    "tamil nadu police", "tamil nadu weather", "tamil nadu election", "tamil nadu transport", 
    "tamil nadu education", "tamil nadu health", "tamil nadu economy", "tamil nadu industry", 
    "tamil nadu agriculture", "tamil nadu rainfall", "tamil nadu cyclone", "tamil nadu flood", 
    "tamil nadu infrastructure", "tamil nadu development",
    # Districts & Cities
    "chennai", "coimbatore", "madurai", "salem", "trichy", "tiruchirappalli", "tirunelveli", 
    "tiruppur", "vellore", "erode", "thanjavur", "thoothukudi", "dindigul", "karur", "namakkal", 
    "krishnagiri", "dharmapuri", "nagapattinam", "mayiladuthurai", "cuddalore", "villupuram", 
    "kallakurichi", "tiruvannamalai", "kanchipuram", "chengalpattu", "tiruvallur", "ranipet", 
    "tirupattur", "ariyalur", "perambalur", "pudukkottai", "ramanathapuram", "sivagangai", 
    "theni", "virudhunagar", "tenkasi", "nilgiris", "kanyakumari", "nagercoil", "pollachi", 
    "hosur", "tambaram", "avadi", "ambattur", "chidambaram", "kumbakonam", "coonoor", "ooty", 
    "udhagamandalam", "tiruchendur", "karaikudi", "sivakasi", "rajapalayam",
    # Context
    "chennai flood", "tamil nadu hospital", "tamil nadu power", "tamil nadu electricity", 
    "tamil nadu water supply", "tamil nadu traffic", "tamil nadu metro", "tamil nadu railway", 
    "tamil nadu highway", "tamil nadu tourism", "tamil nadu temple", "tamil nadu festival"
}

INDIA_KEYWORDS = {
    # Core
    "india", "indian", "national", "nationwide", "central government", "union government", 
    "new delhi", "delhi", "indian economy", "indian market", "india news", "national news", 
    "indian policy", "indian election", "indian parliament", "indian budget", "indian government", 
    "indian supreme court", "indian military", "indian railway", "indian defense", "indian gdp", 
    "indian inflation", "indian stock market",
    # States
    "andhra pradesh", "arunachal pradesh", "assam", "bihar", "chhattisgarh", "goa", "gujarat", 
    "haryana", "himachal pradesh", "jharkhand", "karnataka", "kerala", "madhya pradesh", 
    "maharashtra", "manipur", "meghalaya", "mizoram", "nagaland", "odisha", "punjab", "rajasthan", 
    "sikkim", "telangana", "tripura", "uttar pradesh", "uttarakhand", "west bengal", "puducherry", 
    "ladakh", "jammu and kashmir", "chandigarh", "andaman and nicobar", "lakshadweep", 
    "dadra and nagar haveli", "daman and diu",
    # Cities
    "mumbai", "bangalore", "bengaluru", "hyderabad", "kolkata", "ahmedabad", "pune", "jaipur", 
    "lucknow", "kanpur", "nagpur", "indore", "bhopal", "patna", "surat", "vadodara", "visakhapatnam", 
    "trivandrum", "kochi", "mangalore", "amritsar", "jodhpur", "udaipur", "guwahati", "noida", 
    "gurgaon", "faridabad", "ghaziabad",
    # Events
    "india election", "india budget", "india gdp", "national security", "indian army", "indian navy", 
    "indian air force", "lok sabha", "rajya sabha", "indian election commission", 
    "indian infrastructure", "indian development", "indian reforms", "indian agriculture", 
    "indian industry", "indian technology"
}

WORLD_KEYWORDS = {
    "world", "global", "international", "overseas", "foreign", "abroad", "global news", 
    "worldwide", "international relations", "foreign affairs", "global economy", 
    "global markets", "global conflict", "international summit", "world leaders", 
    "un", "nato", "who", "imf", "world bank", "european union", "g7", "g20", "brics", 
    "asean", "opec", "united states", "usa", "us", "america", "china", "russia", "japan", 
    "germany", "france", "united kingdom", "uk", "canada", "australia", "brazil", "south korea", 
    "north korea", "italy", "spain", "netherlands", "sweden", "norway", "denmark", 
    "finland", "turkey", "iran", "iraq", "israel", "saudi arabia", "uae", "qatar", 
    "kuwait", "south africa", "nigeria", "egypt", "mexico", "argentina", "indonesia", 
    "malaysia", "thailand", "singapore", "vietnam", "philippines", "sri lanka", 
    "bangladesh", "pakistan", "nepal", "bhutan", "afghanistan", "myanmar", "ukraine", 
    "poland", "romania", "greece", "portugal", "switzerland", "austria", "belgium", 
    "ireland", "new zealand", "new york", "washington", "london", "paris", "berlin", 
    "tokyo", "beijing", "shanghai", "moscow", "sydney", "toronto", "dubai", "abu dhabi", 
    "seoul", "bangkok", "kuala lumpur", "rome", "madrid", "barcelona", "chicago", 
    "los angeles", "san francisco", "boston", "houston", "miami", "munich", 
    "frankfurt", "hong kong", "taipei", "global crisis", "international war", "foreign policy", 
    "world economy", "global trade", "international sanctions", "world summit", "climate change", 
    "global recession", "global pandemic", "international agreement", "global energy crisis", 
    "world conflict", "international diplomacy", "global supply chain", "global security", 
    "international law", "global migration", "global finance"
}

CONTEXT_KEYWORDS = {
    "flood", "earthquake", "cyclone", "storm", "rainfall", "landslide", "heatwave", 
    "drought", "fire", "explosion", "accident", "crash", "collapse", "emergency", 
    "rescue", "evacuation", "government", "minister", "chief minister", "prime minister", 
    "policy", "law", "court", "election", "budget", "parliament", "assembly", "administration", 
    "authority", "department", "committee", "economy", "inflation", "gdp", "stock market", 
    "bank", "finance", "trade", "industry", "business", "investment", "export", "import", 
    "manufacturing", "employment", "tax", "revenue"
}

def _has_keyword(text: str, keywords: set) -> str:
    # Use exact word boundaries for short/ambiguous words 
    # Or just standard regex word boundary search to be safe for all
    for kw in keywords:
        if re.search(r'\b' + re.escape(kw) + r'\b', text):
            return kw
    return ""

def detect_region_for_article(article: dict) -> tuple[str, str]:
    """
    Returns (location_string, region_string)
    """
    entities = article.get("entities", [])
    locations = []
    
    # Extract locations from NER
    for ent in entities:
        if ent.get("label") in ["GPE", "LOC", "FAC", "ORG"]:
            locations.append(ent["text"])
            
    # Fallback text
    text = (article.get("title", "") + " " + article.get("description", "")).lower()
    
    # Evaluate region logic
    full_search_text = (", ".join(locations).lower() + " " + text)
    
    # 1. Check Tamil Nadu
    matched_tn = _has_keyword(full_search_text, TN_KEYWORDS)
    if matched_tn:
        return (matched_tn.title(), "tamilnadu")
            
    # 2. Check India
    matched_in = _has_keyword(full_search_text, INDIA_KEYWORDS)
    if matched_in:
        return ("India" if matched_in == "india" else matched_in.title(), "india")
            
    # 3. Check World (if there's a strong world keyword, or fallback)
    matched_world = _has_keyword(full_search_text, WORLD_KEYWORDS)
    if matched_world:
        return (matched_world.title(), "world")
        
    # 4. Global Fallback
    loc = locations[0] if locations else "Global"
    return (loc.title(), "world")

def classify_regions(articles: list[dict]) -> list[dict]:
    """Enrich articles with location and region fields."""
    counts = {"tamilnadu": 0, "india": 0, "world": 0}
    for item in articles:
        loc, reg = detect_region_for_article(item)
        item["location"] = loc
        item["region"] = reg
        counts[reg] += 1
        
    logger.info("✓ Classified %d articles: %d TN, %d India, %d World", 
                len(articles), counts["tamilnadu"], counts["india"], counts["world"])
    return articles
