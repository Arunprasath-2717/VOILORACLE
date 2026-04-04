-- VEILORACLE Supabase Production Schema
-- Optimized for Real-Time Intelligence, Speed, and Scalability

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. REGIONS TABLE
-- Stores supported geographic regions with strict priority.
CREATE TABLE IF NOT EXISTS regions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    priority INTEGER NOT NULL
);

INSERT INTO regions (name, priority) VALUES 
    ('World', 3), 
    ('India', 2), 
    ('Tamil Nadu', 1)
ON CONFLICT (name) DO NOTHING;

-- 2. SOURCES TABLE
-- Tracks news source credibility and performance.
CREATE TABLE IF NOT EXISTS sources (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    credibility_score NUMERIC(3, 2) DEFAULT 0.80
);

-- 3. ARTICLES TABLE
-- Stores all incoming news directly from the classification pipeline.
CREATE TABLE IF NOT EXISTS articles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    description TEXT,
    source VARCHAR(255) REFERENCES sources(name) ON UPDATE CASCADE ON DELETE SET NULL,
    location VARCHAR(255) DEFAULT 'Unknown',
    region VARCHAR(255) REFERENCES regions(name) ON UPDATE CASCADE ON DELETE SET DEFAULT DEFAULT 'World',
    published_at TIMESTAMPTZ NOT NULL,
    confidence NUMERIC(3, 2) DEFAULT 0.00,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    url TEXT,
    UNIQUE(title, source) -- Strict deduplication rule enforces no duplicate title+source combos
);

-- 4. EVENTS TABLE
-- Stores clustered intelligence events.
CREATE TABLE IF NOT EXISTS events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    region VARCHAR(255) REFERENCES regions(name) ON UPDATE CASCADE ON DELETE SET DEFAULT DEFAULT 'World',
    importance_score NUMERIC(5, 2) DEFAULT 0.00,
    article_count INTEGER DEFAULT 1,
    sentiment VARCHAR(50) DEFAULT 'Neutral',
    last_updated TIMESTAMPTZ DEFAULT NOW()
);

-- 5. LOGS TABLE
-- Centralized logging for API failures, DB issues, and connectivity.
CREATE TABLE IF NOT EXISTS logs (
    id SERIAL PRIMARY KEY,
    event TEXT NOT NULL,
    status VARCHAR(50) NOT NULL, -- e.g., 'SUCCESS', 'ERROR', 'WARNING'
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    details JSONB DEFAULT '{}'::jsonb
);

-- ── INDEXES for Performance ─────────────────────────────────────────────
CREATE INDEX idx_articles_region ON articles(region);
CREATE INDEX idx_articles_published_at ON articles(published_at DESC);
CREATE INDEX idx_articles_source ON articles(source);
CREATE INDEX idx_events_region ON events(region);
CREATE INDEX idx_events_updated ON events(last_updated DESC);
CREATE INDEX idx_logs_timestamp ON logs(timestamp DESC);

-- ── REAL-TIME CONFIGURATION ──────────────────────────────────────────────
-- Enable replication for live UI updates via Supabase WebSockets
ALTER PUBLICATION supabase_realtime ADD TABLE articles;
ALTER PUBLICATION supabase_realtime ADD TABLE events;

-- ── ROW-LEVEL SECURITY (RLS) ─────────────────────────────────────────────
-- Protect database from unauthorized client modifications
ALTER TABLE articles ENABLE ROW LEVEL SECURITY;
ALTER TABLE events ENABLE ROW LEVEL SECURITY;
ALTER TABLE logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE regions ENABLE ROW LEVEL SECURITY;
ALTER TABLE sources ENABLE ROW LEVEL SECURITY;

-- Allow anonymous read access for UI
CREATE POLICY "Allow public read access to articles" ON articles FOR SELECT USING (true);
CREATE POLICY "Allow public read access to events" ON events FOR SELECT USING (true);
CREATE POLICY "Allow public read access to regions" ON regions FOR SELECT USING (true);

-- Backend service role (via API key bypasses RLS) handles inserts/updates.
