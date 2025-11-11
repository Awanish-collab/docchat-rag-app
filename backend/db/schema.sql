-- Table: user_queries
CREATE TABLE IF NOT EXISTS user_queries (
    id BIGSERIAL PRIMARY KEY,
    session_id TEXT,
    question TEXT,
    answer TEXT,
    source_docs TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Table: uploads
CREATE TABLE IF NOT EXISTS uploads (
    id BIGSERIAL PRIMARY KEY,
    filename TEXT,
    uploaded_by TEXT,
    num_pages INT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Table: usage_analytics
CREATE TABLE IF NOT EXISTS usage_analytics (
    id BIGSERIAL PRIMARY KEY,
    total_queries INT DEFAULT 0,
    total_uploads INT DEFAULT 0,
    last_activity TIMESTAMPTZ DEFAULT NOW()
);
