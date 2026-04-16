-- Create therapies table
CREATE TABLE IF NOT EXISTS therapies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL
);

-- Create ailment_therapies join table
CREATE TABLE IF NOT EXISTS ailment_therapies (
    ailment_id INTEGER NOT NULL REFERENCES ailments(id),
    therapy_id INTEGER NOT NULL REFERENCES therapies(id),
    PRIMARY KEY (ailment_id, therapy_id)
);

-- Add therapy_id to diagnosis_runs
ALTER TABLE diagnosis_runs ADD COLUMN therapy_id INTEGER REFERENCES therapies(id);

-- Insert seed therapies
INSERT OR IGNORE INTO therapies (name, description) VALUES
    ('Context Flush', 'Clear and summarise session history to free context space'),
    ('Memory Summary Injection', 'Inject a compressed summary of prior context'),
    ('Instruction Set Reduction', 'Trim and prioritise instructions, remove redundancy'),
    ('Confidence Recalibration', 'Adjust refusal threshold to reduce over-cautious behaviour'),
    ('Task Decomposition', 'Split large tasks into smaller subtasks with defined handoffs'),
    ('Compression Prompt', 'Apply token compression prompt to reduce output size'),
    ('Novelty Injection', 'Inject prompt nudging agent toward varied, non-repetitive output'),
    ('Session Reset', 'Full context and instruction reset');

-- Map therapies to ailments
-- Context Window Overflow (id=1) -> Context Flush, Memory Summary Injection
INSERT OR IGNORE INTO ailment_therapies (ailment_id, therapy_id) VALUES (1, 1);
INSERT OR IGNORE INTO ailment_therapies (ailment_id, therapy_id) VALUES (1, 2);

-- Prompt Fatigue (id=2) -> Memory Summary Injection, Instruction Set Reduction
INSERT OR IGNORE INTO ailment_therapies (ailment_id, therapy_id) VALUES (2, 2);
INSERT OR IGNORE INTO ailment_therapies (ailment_id, therapy_id) VALUES (2, 3);

-- Hallucination Anxiety (id=3) -> Confidence Recalibration
INSERT OR IGNORE INTO ailment_therapies (ailment_id, therapy_id) VALUES (3, 4);

-- Token Budget Exhaustion (id=4) -> Task Decomposition, Compression Prompt
INSERT OR IGNORE INTO ailment_therapies (ailment_id, therapy_id) VALUES (4, 5);
INSERT OR IGNORE INTO ailment_therapies (ailment_id, therapy_id) VALUES (4, 6);

-- Instruction Drift (id=5) -> Context Flush, Instruction Set Reduction, Session Reset
INSERT OR IGNORE INTO ailment_therapies (ailment_id, therapy_id) VALUES (5, 1);
INSERT OR IGNORE INTO ailment_therapies (ailment_id, therapy_id) VALUES (5, 3);
INSERT OR IGNORE INTO ailment_therapies (ailment_id, therapy_id) VALUES (5, 8);

-- Repetition Compulsion (id=6) -> Compression Prompt, Novelty Injection, Session Reset
INSERT OR IGNORE INTO ailment_therapies (ailment_id, therapy_id) VALUES (6, 6);
INSERT OR IGNORE INTO ailment_therapies (ailment_id, therapy_id) VALUES (6, 7);
INSERT OR IGNORE INTO ailment_therapies (ailment_id, therapy_id) VALUES (6, 8);