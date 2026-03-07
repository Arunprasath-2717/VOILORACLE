#!/usr/bin/env python3
"""Quick test of data collection from all sources."""

import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s'
)

from backend.collector import collect_news

print("\n" + "="*70)
print("VEILORACLE — Data Collection Test")
print("="*70)

try:
    articles = collect_news()
    print(f"\n✓ Total articles collected: {len(articles)}\n")
    
    for i, a in enumerate(articles[:5]):
        print(f"{i+1}. {a.get('title', 'N/A')[:80]}...")
        print(f"   Source: {a.get('source', 'N/A')}")
        print(f"   URL: {a.get('url', 'N/A')[:60]}")
        print()
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("="*70)
print("✓ Collection test successful!")
print("="*70)
