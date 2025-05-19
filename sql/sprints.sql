-- Create sprints table
CREATE TABLE IF NOT EXISTS sprints (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    goal TEXT,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'Planned',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

-- Insert mock sprints
INSERT INTO sprints (name, goal, start_date, end_date, status, created_at) VALUES
('Sprint 1', 'Set up the foundation for the mobile app and implement basic authentication.', CURRENT_DATE - INTERVAL '14 days', CURRENT_DATE + INTERVAL '0 days', 'In Progress', CURRENT_TIMESTAMP - INTERVAL '15 days'),

('Sprint 2', 'Implement field data collection forms and begin work on offline mode.', CURRENT_DATE + INTERVAL '1 day', CURRENT_DATE + INTERVAL '15 days', 'Planned', CURRENT_TIMESTAMP - INTERVAL '10 days'),

('Sprint 3', 'Complete offline mode and implement data synchronization.', CURRENT_DATE + INTERVAL '16 days', CURRENT_DATE + INTERVAL '30 days', 'Planned', CURRENT_TIMESTAMP - INTERVAL '10 days'),

('Sprint 4', 'Implement customer feedback submission interface and begin work on the management dashboard.', CURRENT_DATE + INTERVAL '1 day', CURRENT_DATE + INTERVAL '15 days', 'Planned', CURRENT_TIMESTAMP - INTERVAL '5 days'),

('Sprint 5', 'Set up the knowledge base structure and begin content migration.', CURRENT_DATE - INTERVAL '30 days', CURRENT_DATE - INTERVAL '16 days', 'Completed', CURRENT_TIMESTAMP - INTERVAL '35 days');
