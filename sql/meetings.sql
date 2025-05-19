-- Create meeting_types enum
CREATE TYPE meeting_type AS ENUM ('standup', 'sprint_planning', 'sprint_review', 'sprint_retrospective', 'other');

-- Create meeting_status enum
CREATE TYPE meeting_status AS ENUM ('scheduled', 'in_progress', 'completed', 'cancelled');

-- Create meetings table
CREATE TABLE IF NOT EXISTS meetings (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    meeting_type meeting_type NOT NULL,
    status meeting_status NOT NULL DEFAULT 'scheduled',
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    location VARCHAR(255),
    virtual_meeting_url VARCHAR(1024),
    sprint_id INTEGER,
    created_by VARCHAR(36) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (sprint_id) REFERENCES sprints (id) ON DELETE SET NULL,
    FOREIGN KEY (created_by) REFERENCES users (id)
);

-- Insert mock meetings
INSERT INTO meetings (title, description, meeting_type, status, start_time, end_time, location, virtual_meeting_url, sprint_id, created_by, created_at) VALUES
('Daily Standup - Mobile App Team', 'Daily standup meeting for the mobile app development team.', 'standup', 'scheduled', CURRENT_TIMESTAMP + INTERVAL '1 day' + INTERVAL '9 hours', CURRENT_TIMESTAMP + INTERVAL '1 day' + INTERVAL '9 hours 15 minutes', 'Virtual', 'https://meet.example.com/standup-mobile', 1, '00000000-0000-0000-0000-000000000006', CURRENT_TIMESTAMP - INTERVAL '14 days'),

('Sprint 1 Planning', 'Planning meeting for Sprint 1 of the Mobile App project.', 'sprint_planning', 'completed', CURRENT_TIMESTAMP - INTERVAL '14 days', CURRENT_TIMESTAMP - INTERVAL '14 days' + INTERVAL '2 hours', 'Conference Room A', 'https://meet.example.com/sprint1-planning', 1, '00000000-0000-0000-0000-000000000006', CURRENT_TIMESTAMP - INTERVAL '15 days'),

('Sprint 1 Review', 'Review meeting for Sprint 1 of the Mobile App project.', 'sprint_review', 'scheduled', CURRENT_TIMESTAMP + INTERVAL '1 day' + INTERVAL '14 hours', CURRENT_TIMESTAMP + INTERVAL '1 day' + INTERVAL '15 hours', 'Conference Room A', 'https://meet.example.com/sprint1-review', 1, '00000000-0000-0000-0000-000000000006', CURRENT_TIMESTAMP - INTERVAL '5 days'),

('Sprint 1 Retrospective', 'Retrospective meeting for Sprint 1 of the Mobile App project.', 'sprint_retrospective', 'scheduled', CURRENT_TIMESTAMP + INTERVAL '1 day' + INTERVAL '15 hours 30 minutes', CURRENT_TIMESTAMP + INTERVAL '1 day' + INTERVAL '16 hours 30 minutes', 'Conference Room B', 'https://meet.example.com/sprint1-retro', 1, '00000000-0000-0000-0000-000000000006', CURRENT_TIMESTAMP - INTERVAL '5 days'),

('Sprint 2 Planning', 'Planning meeting for Sprint 2 of the Mobile App project.', 'sprint_planning', 'scheduled', CURRENT_TIMESTAMP + INTERVAL '2 days' + INTERVAL '10 hours', CURRENT_TIMESTAMP + INTERVAL '2 days' + INTERVAL '12 hours', 'Conference Room A', 'https://meet.example.com/sprint2-planning', 2, '00000000-0000-0000-0000-000000000006', CURRENT_TIMESTAMP - INTERVAL '5 days'),

('Knowledge Base Kickoff', 'Kickoff meeting for the Knowledge Base project.', 'other', 'completed', CURRENT_TIMESTAMP - INTERVAL '30 days', CURRENT_TIMESTAMP - INTERVAL '30 days' + INTERVAL '1 hour', 'Conference Room C', 'https://meet.example.com/kb-kickoff', 5, '00000000-0000-0000-0000-000000000003', CURRENT_TIMESTAMP - INTERVAL '35 days'),

('Daily Standup - Knowledge Base Team', 'Daily standup meeting for the knowledge base team.', 'standup', 'scheduled', CURRENT_TIMESTAMP + INTERVAL '1 day' + INTERVAL '9 hours 30 minutes', CURRENT_TIMESTAMP + INTERVAL '1 day' + INTERVAL '9 hours 45 minutes', 'Virtual', 'https://meet.example.com/standup-kb', 5, '00000000-0000-0000-0000-000000000006', CURRENT_TIMESTAMP - INTERVAL '35 days');
