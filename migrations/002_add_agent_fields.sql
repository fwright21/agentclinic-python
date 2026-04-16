-- Add new columns to agents table
ALTER TABLE agents ADD COLUMN reasoning_level TEXT;
ALTER TABLE agents ADD COLUMN skills TEXT;
ALTER TABLE agents ADD COLUMN tools TEXT;
ALTER TABLE agents ADD COLUMN mcps TEXT;

-- Update seed agents with new field values
UPDATE agents SET 
    name = 'Pepper-Bot',
    model_type = 'ollama/qwen2.5',
    reasoning_level = 'low',
    status = 'Resolved',
    skills = 'affirmation-generation,scheduling',
    tools = 'telegram,apscheduler',
    mcps = '',
    presenting_complaints = 'Repeated affirmation sent twice in same day'
WHERE id = 1;

UPDATE agents SET 
    name = 'Briefing-Agent',
    model_type = 'groq/llama-3.3',
    reasoning_level = 'medium',
    status = 'Recurring',
    skills = 'summarisation,semantic-search,extraction',
    tools = 'telegram,chat.py',
    mcps = 'mcp-memory',
    presenting_complaints = 'Token budget exceeded on evening digest'
WHERE id = 2;

UPDATE agents SET 
    name = 'LinguistDebate-A',
    model_type = 'gpt-5.2',
    reasoning_level = 'high',
    status = 'Chronic',
    skills = 'compression,review,benchmarking',
    tools = 'codex-cli,deepeval',
    mcps = '',
    presenting_complaints = 'Quality drop on definition queries after compression'
WHERE id = 3;

UPDATE agents SET 
    name = 'A2A-Coordinator',
    model_type = 'gpt-5.3',
    reasoning_level = 'xhigh',
    status = 'Active',
    skills = 'coordination,protocol-design',
    tools = 'run_tests.py',
    mcps = '',
    presenting_complaints = 'Repair turns spiking on PCL-1 protocol runs'
WHERE id = 4;

UPDATE agents SET 
    name = 'ClaudeBot-7',
    model_type = 'claude-sonnet-4.6',
    reasoning_level = 'medium',
    status = 'Unknown',
    skills = 'planning,debugging,architecture',
    tools = 'bash,file_read',
    mcps = 'mcp-registry',
    presenting_complaints = 'No recent activity logged'
WHERE id = 5;