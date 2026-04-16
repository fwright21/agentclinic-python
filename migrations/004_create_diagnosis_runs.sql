CREATE TABLE IF NOT EXISTS diagnosis_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id INTEGER NOT NULL REFERENCES agents(id),
    ailment_id INTEGER REFERENCES ailments(id),
    submitted_symptoms TEXT NOT NULL,
    report TEXT NOT NULL,
    prompt_tokens INTEGER,
    completion_tokens INTEGER,
    total_tokens INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
