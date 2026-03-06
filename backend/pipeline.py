"""
VEILORACLE — Pipeline Orchestrator (Complete AI Edition)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
End-to-end: collect → preprocess → detect → sentiment → NER → sector route
          → model route → summarize → predict → intelligence → anomaly → trends → store.
"""

import logging
import time
import uuid
import json
from typing import Dict, List, Any
from datetime import datetime

from backend import config  # type: ignore
from backend import database  # type: ignore
from backend import collector  # type: ignore
from backend import preprocessor  # type: ignore
from backend import detector  # type: ignore
from backend import sentiment  # type: ignore
from backend import predictor  # type: ignore
from backend import summarizer  # type: ignore
from backend import ner_engine  # type: ignore
from backend import trend_engine  # type: ignore
from backend import anomaly_engine  # type: ignore
from backend import intelligence  # type: ignore
from backend import sector_router  # type: ignore
from backend import model_router  # type: ignore
from backend import fake_news  # type: ignore
from backend import topic_discovery  # type: ignore
from backend import multilingual  # type: ignore
from backend import queue_manager  # type: ignore
import threading

logger = logging.getLogger("veiloracle.pipeline")


def _collector_worker():
    while True:
        try:
            articles = collector.collect_news()
            queue_manager.push_articles(articles)
        except Exception as e:
            logger.error("Collector thread error: %s", e)
        time.sleep(config.FETCH_INTERVAL_SECONDS)

def run_pipeline(one_shot: bool = True):
    database.init_db()
    logger.info("=" * 60)
    logger.info("VEILORACLE Intelligence Pipeline — Streaming Starting")
    logger.info("=" * 60)
    
    if not one_shot:
        t = threading.Thread(target=_collector_worker, daemon=True)
        t.start()
        logger.info("Background collector thread started.")
    elif one_shot:
        queue_manager.push_articles(collector.collect_news())

    iteration: int = 0
    while True:
        iteration = iteration + 1
        hex_str: str = uuid.uuid4().hex
        hex_short: str = "".join([hex_str[i] for i in range(min(6, len(hex_str)))])
        run_id: str = "run_" + datetime.utcnow().strftime("%Y%m%d_%H%M%S") + "_" + hex_short
        logger.info("─" * 60)
        logger.info("Pipeline Run #%d  [%s]", iteration, run_id)
        logger.info("─" * 60)

        database.start_pipeline_run(run_id)

        try:
            # STEP 1: Process items from stream
            logger.info("▸ Step 1: Popping from message queue...")
            articles = queue_manager.pop_articles(batch_size=50)
            if not articles:
                if one_shot: break
                time.sleep(5)
                continue

            # STEP 2: Preprocessing & New NLP
            logger.info("▸ Step 2: NLP Preprocessing (clean, fake news, multilingual)...")
            articles = preprocessor.preprocess_articles(articles)
            articles = fake_news.analyze_articles_fake_news(articles)
            articles = multilingual.process_articles_multilingual(articles)

            # STEP 3: Event Detection (Embeddings + HDBSCAN + Duplicate removal)
            logger.info("▸ Step 3: AI Event Detection (Embeddings + HDBSCAN)...")
            events = detector.detect_events(articles)

            # STEP 4: Sentiment Analysis (RoBERTa)
            logger.info("▸ Step 4/12: AI Sentiment Analysis (RoBERTa NLP)...")
            articles = sentiment.analyze_articles(articles)

            # STEP 5: Named Entity Recognition (spaCy)
            logger.info("▸ Step 5/12: AI Named Entity Recognition (spaCy NER)...")
            articles = ner_engine.enrich_articles_with_entities(articles)
            ner_results = ner_engine.extract_from_articles(articles)

            # STEP 6: Sector Classification (Keyword Router)
            logger.info("▸ Step 6/12: Sector Classification (Intelligent Routing)...")
            articles = sector_router.route_articles(articles)

            # STEP 7: Sector-Specific AI Model Routing
            logger.info("▸ Step 7/12: AI Model Routing (FinBERT/Qwen2/Mistral/DeepSeek/BioGPT/Llama3)...")
            articles = model_router.route_and_analyze(articles)

            # STEP 8: AI Summarization (BART Transformer)
            logger.info("▸ Step 8/12: AI Summarization (BART Transformer)...")
            events = summarizer.summarize_events(events, articles)

            # STEP 9: Impact Prediction (Sector Matching)
            logger.info("▸ Step 9/12: AI Impact Prediction (Sector Analysis)...")
            articles = predictor.predict_impacts(articles)

            # STEP 10: Intelligence Engine (Scores & Impacts)
            logger.info("▸ Step 10/12: Intelligence Engine (Importance & Risk)...")
            events = intelligence.compute_intelligence(events, articles)

            # STEP 11: Anomaly Detection (Z-Score)
            logger.info("▸ Step 11/12: AI Anomaly Detection (Z-Score Analysis)...")
            anomaly_results = anomaly_engine.run_anomaly_detection(articles)

            # STEP 12: Trend Forecasting (Linear Regression)
            logger.info("▸ Step 12: AI Trend Forecasting (Linear Regression)...")
            trend_results = trend_engine.analyze_sector_trends(articles)
            top_movers = trend_engine.get_top_movers(trend_results)
            
            # STEP 13: Topic Discovery
            logger.info("▸ Step 13: Dynamic Topic Discovery (BERTopic)...")
            topics = topic_discovery.discover_topics(articles)

            # Generate Intelligence Output (structured JSON per event)
            logger.info("▸ Generating structured intelligence output...")
            intelligence_output = model_router.generate_all_intelligence(events, articles)

            # SAVE to Database
            logger.info("▸ Saving to database...")
            article_ids = database.save_articles(articles, run_id)
            database.save_events(events, article_ids, articles, run_id)
            database.save_impacts(articles, article_ids, run_id)
            database.finish_pipeline_run(run_id, len(articles), len(events))

            # Log Results
            logger.info("═" * 60)
            logger.info("✓ Run #%d Complete — %d articles, %d events", iteration, len(articles), len(events))
            logger.info("  🧠 NER: %d unique entities extracted", len(ner_results.get("entities", [])))
            logger.info("  🔍 Anomalies: %d critical, %d warnings",
                        anomaly_results["critical_count"], anomaly_results["warning_count"])
            logger.info("  📈 Trends: %d rising, %d falling sectors",
                        len(top_movers["rising"]), len(top_movers["falling"]))

            # Log sector distribution
            sector_dist = sector_router.get_sector_distribution(articles)
            logger.info("  🏷️ Sector Distribution:")
            for sec, cnt in sorted(sector_dist.items(), key=lambda x: -x[1]):
                logger.info("      %s: %d articles", sec, cnt)

            # Log model routing stats
            model_info = model_router.get_model_info()
            logger.info("  🤖 AI Models:")
            for sec, info in model_info.items():
                status = "✅ loaded" if info["loaded"] else "⚙️ available" if info["hf_api_available"] else "🔧 fallback"
                logger.info("      %s → %s [%s]", sec, info["model_id"], status)

            if intelligence_output:
                logger.info("  📊 Topics Discovered: %d", len(topics.get("topics", [])))
                sample: Dict[str, Any] = intelligence_output[0]
                logger.info("  📊 Sample Intelligence Output:")
                sample_title: str = str(sample.get("event_title", ""))
                if len(sample_title) > 80:
                    sample_title = "".join([sample_title[ci] for ci in range(80)])
                logger.info("      Title: %s", sample_title)
                logger.info("      Sector: %s | Sentiment: %s", sample.get("sector"), sample.get("sentiment"))
                logger.info("      Importance: %.1f | Risk: %.1f",
                            sample.get("importance_score", 0), sample.get("risk_score", 0))
                impacted_secs: List[str] = sample.get("impacted_sectors", [])
                top_secs: List[str] = []
                si2: int = 0
                while si2 < min(5, len(impacted_secs)):
                    top_secs.append(impacted_secs[si2])
                    si2 = si2 + 1
                logger.info("      Impacted Sectors: %s", ", ".join(top_secs))

            sector_summary: Dict[str, Any] = predictor.summarize_sector_impacts(articles)
            sorted_summary: List[Any] = sorted(sector_summary.items())
            top_summary: List[Any] = []
            ss_idx: int = 0
            while ss_idx < min(10, len(sorted_summary)):
                top_summary.append(sorted_summary[ss_idx])
                ss_idx = ss_idx + 1
            for sec, data in top_summary:
                logger.info("  %s %s (mentions: %d)", data["net_direction"], sec, data["total_mentions"])

            sc: Dict[str, int] = {"Positive": 0, "Negative": 0, "Neutral": 0}
            for a in articles:
                sent_label: str = str(a.get("sentiment", {}).get("label", "Neutral"))
                sc[sent_label] = sc.get(sent_label, 0) + 1
            logger.info("  🟢 %d positive  🔴 %d negative  🟡 %d neutral", sc["Positive"], sc["Negative"], sc["Neutral"])
            logger.info("═" * 60)

        except Exception as e:
            logger.error("Pipeline failed: %s", e, exc_info=True)
            database.finish_pipeline_run(run_id, 0, 0, "error", str(e))

        if one_shot: break
        logger.info("Next run in %ds...", config.FETCH_INTERVAL_SECONDS)
        time.sleep(config.FETCH_INTERVAL_SECONDS)

    logger.info("Pipeline finished.")
