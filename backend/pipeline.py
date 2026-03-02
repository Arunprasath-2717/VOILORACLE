"""
VEILORACLE — Pipeline Orchestrator (Complete AI Edition)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
End-to-end: collect → preprocess → detect → sentiment → NER → summarize → predict → anomaly → trends → store.
"""

import logging
import time
import uuid
from datetime import datetime

from backend import config
from backend import database
from backend import collector
from backend import preprocessor
from backend import detector
from backend import sentiment
from backend import predictor
from backend import summarizer
from backend import ner_engine
from backend import trend_engine
from backend import anomaly_engine
from backend import intelligence

logger = logging.getLogger("veiloracle.pipeline")


def run_pipeline(one_shot: bool = True):
    database.init_db()
    logger.info("=" * 60)
    logger.info("VEILORACLE Intelligence Pipeline — Starting (Full AI Mode)")
    logger.info("=" * 60)

    iteration = 0
    while True:
        iteration += 1
        run_id = f"run_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
        logger.info("─" * 60)
        logger.info("Pipeline Run #%d  [%s]", iteration, run_id)
        logger.info("─" * 60)

        database.start_pipeline_run(run_id)

        try:
            # STEP 1: Collect News
            logger.info("▸ Step 1/9: Collecting news...")
            articles = collector.collect_news()
            if not articles:
                database.finish_pipeline_run(run_id, 0, 0, "skipped", "No articles")
                if one_shot: break
                time.sleep(config.FETCH_INTERVAL_SECONDS); continue

            # STEP 2: NLP Preprocessing
            logger.info("▸ Step 2/9: NLP Preprocessing (tokenize, stopwords, clean)...")
            articles = preprocessor.preprocess_articles(articles)

            # STEP 3: Event Detection (Sentence Embeddings + DBSCAN)
            logger.info("▸ Step 3/9: AI Event Detection (Embeddings + DBSCAN)...")
            events = detector.detect_events(articles)

            # STEP 4: Sentiment Analysis (VADER)
            logger.info("▸ Step 4/9: AI Sentiment Analysis (VADER NLP)...")
            articles = sentiment.analyze_articles(articles)

            # STEP 5: Named Entity Recognition (spaCy)
            logger.info("▸ Step 5/9: AI Named Entity Recognition (spaCy NER)...")
            articles = ner_engine.enrich_articles_with_entities(articles)
            ner_results = ner_engine.extract_from_articles(articles)

            # STEP 6: AI Summarization (BART Transformer)
            logger.info("▸ Step 6/9: AI Summarization (BART Transformer)...")
            events = summarizer.summarize_events(events, articles)

            # STEP 7: Impact Prediction (Sector Matching)
            logger.info("▸ Step 7/10: AI Impact Prediction (Sector Analysis)...")
            articles = predictor.predict_impacts(articles)

            # STEP 8: Intelligence Engine (Scores & Impacts)
            logger.info("▸ Step 8/10: Intelligence Engine (Importance & Risk)...")
            events = intelligence.compute_intelligence(events, articles)

            # STEP 9: Anomaly Detection (Z-Score)
            logger.info("▸ Step 9/10: AI Anomaly Detection (Z-Score Analysis)...")
            anomaly_results = anomaly_engine.run_anomaly_detection(articles)

            # STEP 10: Trend Forecasting (Linear Regression)
            logger.info("▸ Step 10/10: AI Trend Forecasting (Linear Regression)...")
            trend_results = trend_engine.analyze_sector_trends(articles)
            top_movers = trend_engine.get_top_movers(trend_results)

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

            sector_summary = predictor.summarize_sector_impacts(articles)
            for sec, data in list(sorted(sector_summary.items()))[:10]:
                logger.info("  %s %s (mentions: %d)", data["net_direction"], sec, data["total_mentions"])

            sc = {"Positive": 0, "Negative": 0, "Neutral": 0}
            for a in articles:
                sc[a.get("sentiment", {}).get("label", "Neutral")] += 1
            logger.info("  🟢 %d positive  🔴 %d negative  🟡 %d neutral", sc["Positive"], sc["Negative"], sc["Neutral"])
            logger.info("═" * 60)

        except Exception as e:
            logger.error("Pipeline failed: %s", e, exc_info=True)
            database.finish_pipeline_run(run_id, 0, 0, "error", str(e))

        if one_shot: break
        logger.info("Next run in %ds...", config.FETCH_INTERVAL_SECONDS)
        time.sleep(config.FETCH_INTERVAL_SECONDS)

    logger.info("Pipeline finished.")
