-- Create agents table
CREATE TABLE IF NOT EXISTS agents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    model_type TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Unknown',
    presenting_complaints TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Seed 5 agents
INSERT OR IGNORE INTO agents (name, model_type, status, presenting_complaints) VALUES
    ('GPT-4-Agent-01', 'gpt-4', 'Active', 'Hallucination on factual queries'),
    ('ClaudeBot-7', 'claude-3', 'Chronic', 'Repeated context window overflow'),
    ('Gemini-Probe-3', 'gemini-pro', 'Resolved', 'Prompt fatigue after long sessions'),
    ('MistralX-2', 'mistral-7b', 'Recurring', 'Token budget exceeded on summaries'),
    ('LlamaGuard-9', 'llama-3', 'Unknown', 'No recent activity logged');