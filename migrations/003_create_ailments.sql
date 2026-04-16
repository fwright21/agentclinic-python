CREATE TABLE IF NOT EXISTS ailments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL,
    recommended_treatment TEXT NOT NULL
);

INSERT OR IGNORE INTO ailments (name, description, recommended_treatment) VALUES
    ('Context Window Overflow', 'Agent loses earlier information mid-session due to context limit', 'Apply context flush and summary injection'),
    ('Prompt Fatigue', 'Degraded output after long or repetitive instruction sets', 'Reduce instruction set, add memory summary'),
    ('Hallucination Anxiety', 'Over-cautious refusals due to over-correction for hallucination', 'Recalibrate confidence threshold, loosen safety constraints'),
    ('Token Budget Exhaustion', 'Agent hits token limits mid-task and truncates output', 'Split task into subtasks, apply compression prompt'),
    ('Instruction Drift', 'Gradual deviation from original instructions over long session', 'Re-inject original instructions, reset session context'),
    ('Repetition Compulsion', 'Agent loops or repeats same output across turns', 'Flush recent history, inject novelty prompt');
