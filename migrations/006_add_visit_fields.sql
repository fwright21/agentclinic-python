-- Phase 9: Visit log + outcomes
ALTER TABLE diagnosis_runs ADD COLUMN outcome TEXT DEFAULT 'OPEN';
ALTER TABLE diagnosis_runs ADD COLUMN visit_number INTEGER;

-- Index for efficient chronic check queries
CREATE INDEX idx_diagnosis_runs_agent_ailment ON diagnosis_runs(agent_id, ailment_id);