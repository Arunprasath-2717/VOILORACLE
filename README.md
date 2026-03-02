# 🔮 VEILORACLE — AI-Powered Global Intelligence Network

> Real-time news intelligence across **ALL** global sectors — finance, technology, sports, entertainment, science, defense, healthcare, environment, education, agriculture, fashion, legal, and more — powered by **9 AI/ML engines**.

---

## 🧠 AI Technologies Used

| # | AI Engine | Library | Purpose |
|---|-----------|---------|---------|
| 1 | **Sentence Embeddings** | `sentence-transformers` (all-MiniLM-L6-v2) | Converts article text → 384-dim vectors for semantic similarity |
| 2 | **DBSCAN Clustering** | `scikit-learn` | Auto-groups similar articles into "event clusters" |
| 3 | **VADER Sentiment** | `nltk.sentiment.vader` | Classifies articles as Positive/Negative/Neutral |
| 4 | **NLP Preprocessing** | `nltk` (tokenize, stopwords) | Cleans and normalizes raw text |
| 5 | **Named Entity Recognition** | `spaCy` (en_core_web_sm) | Extracts people, organizations, locations, money |
| 6 | **AI Summarization** | `transformers` (BART) | Generates concise summaries of events |
| 7 | **Impact Prediction** | Custom (keyword matching) | Maps articles → 3000 sectors, predicts direction |
| 8 | **Anomaly Detection** | `numpy` (z-score) | Detects unusual volume spikes and sentiment shifts |
| 9 | **Trend Forecasting** | `numpy` (linear regression) | Predicts future sentiment direction per sector |

## 🚀 Quick Start

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Download spaCy model (for NER)
python -m spacy download en_core_web_sm

# 3. Install frontend dependencies
cd frontend && npm install && cd ..

# 4. Run the intelligence pipeline (processes news through all 9 AI engines)
python main.py pipeline

# 5. Start the API server (port 8000)
python main.py server

# 6. Start the frontend (port 5173)
python main.py frontend
```

## 📁 Project Structure

```
VEILORACLE EE Project/
├── backend/
│   ├── api.py             # FastAPI endpoints (core + 4 AI endpoints)
│   ├── collector.py        # News collection (NewsAPI + RSS + sample data)
│   ├── config.py           # 3000 sectors across ALL global fields
│   ├── database.py         # SQLite storage layer
│   ├── detector.py         # AI: Sentence Embeddings + DBSCAN clustering
│   ├── pipeline.py         # 9-step AI pipeline orchestrator
│   ├── predictor.py        # AI: Sector impact prediction
│   ├── preprocessor.py     # AI: NLP text preprocessing
│   ├── sentiment.py        # AI: VADER sentiment analysis
│   ├── summarizer.py       # AI: BART transformer summarization
│   ├── ner_engine.py       # AI: spaCy named entity recognition
│   ├── trend_engine.py     # AI: Linear regression trend forecasting
│   └── anomaly_engine.py   # AI: Z-score anomaly detection
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # React app with 6 tabbed AI views
│   │   ├── App.css         # Premium glassmorphism UI styles
│   │   └── index.css       # Base design tokens
│   └── index.html          # SEO-optimized HTML
├── main.py                 # Entry point (pipeline / server / frontend)
├── requirements.txt        # Python dependencies
└── .env.example            # Environment configuration
```

## 🌐 Global Sector Coverage

VEILORACLE monitors **3000+ AI-generated sectors** across every major field:

- 💰 Finance, Banking, Crypto, Insurance, Venture Capital
- 💻 Technology, AI, Cybersecurity, Semiconductors, Cloud
- 🏥 Healthcare, Pharma, Biotech, Mental Health
- ⚡ Energy, Renewables, Oil & Gas, Nuclear
- 🏛️ Politics, Diplomacy, Defense, Law & Justice
- ✈️ Aviation, Shipping, Automotive, Railways
- 🏈 Sports, Olympics, Football, Cricket, Basketball
- 🎬 Entertainment, Film, Music, Gaming, Streaming
- 🔬 Science, Space, Physics, Astronomy
- 🌍 Environment, Climate, Wildlife, Conservation
- 🎓 Education, EdTech, Research, Universities
- 🌾 Agriculture, Food, Fisheries, Organic
- 🏘️ Real Estate, Construction, Housing
- ⚙️ Manufacturing, Robotics, Automation
- 👗 Fashion, Design, Arts, Culture
- ⛏️ Mining, Gold, Lithium, Rare Earth
- ⚖️ Legal, Compliance, Human Rights

## 🖥️ Frontend Features

- **3D Neural Visualization** — Interactive particle sphere (Three.js/React Three Fiber)
- **AI Intelligence Briefing** — Real-time market mood analysis
- **6 Tabbed Views** — Overview, Sectors, Events, NER Entities, AI Trends, Anomalies
- **Entity Cloud** — AI-extracted people, organizations, locations
- **Trend Forecasting** — Rising/falling sector predictions with confidence scores
- **Anomaly Alerts** — Critical and warning alerts with severity indicators
- **Glassmorphism UI** — Premium dark theme with micro-animations
