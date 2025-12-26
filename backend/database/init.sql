"""
Database initialization and setup scripts.
"""

-- Create database
CREATE DATABASE IF NOT EXISTS reputation_ai;

-- Connect to database
\c reputation_ai;

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For text search

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_trgm_mentions_content ON mentions USING gin(content gin_trgm_ops);

-- Create function for updating timestamps
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Initial data population can be added here
INSERT INTO users (email, username, hashed_password, full_name, role, is_active, is_verified, gdpr_consent)
VALUES 
    ('admin@aiguardian.com', 'admin', '$2b$12$placeholder_hash', 'System Administrator', 'super_admin', true, true, true)
ON CONFLICT (email) DO NOTHING;

-- Grant permissions (adjust based on your setup)
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;
