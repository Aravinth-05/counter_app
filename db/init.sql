-- init.sql -- Runs once when PostgreSQL starts for the first time
--
-- This creates our database, table, and inserts a starting row.
-- In Phase 3 (Docker), this file gets mounted into the PostgreSQL
-- container so the database is ready to go immediately.

-- Create the counters table
CREATE TABLE IF NOT EXISTS counters (
    id SERIAL PRIMARY KEY,           -- Auto-incrementing ID
    name VARCHAR(50) UNIQUE NOT NULL, -- Counter name (we use "main")
    value INTEGER NOT NULL DEFAULT 0, -- The actual count
    updated_at TIMESTAMPTZ DEFAULT NOW() -- Last update timestamp
);

-- Insert the default counter row
INSERT INTO counters (name, value)
VALUES ('main', 0)
ON CONFLICT (name) DO NOTHING;       -- Don't error if it already exists
