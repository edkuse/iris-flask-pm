-- Create epics table
CREATE TABLE IF NOT EXISTS epics (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) NOT NULL DEFAULT 'Not Started',
    priority VARCHAR(50),
    product_idea_id INTEGER,
    creator_id VARCHAR(36) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (product_idea_id) REFERENCES product_ideas (id) ON DELETE SET NULL,
    FOREIGN KEY (creator_id) REFERENCES users (id)
);

-- Insert mock epics
INSERT INTO epics (title, description, status, priority, product_idea_id, creator_id, created_at) VALUES
('Mobile App Authentication', 'Implement secure authentication for the mobile app, including biometric options.', 'In Progress', 'High', 1, '00000000-0000-0000-0000-000000000003', CURRENT_TIMESTAMP - INTERVAL '28 days'),

('Field Data Collection', 'Create forms and workflows for field workers to collect and submit data.', 'Not Started', 'Medium', 1, '00000000-0000-0000-0000-000000000003', CURRENT_TIMESTAMP - INTERVAL '27 days'),

('Offline Mode Support', 'Enable the app to work offline and sync data when connectivity is restored.', 'Not Started', 'High', 1, '00000000-0000-0000-0000-000000000002', CURRENT_TIMESTAMP - INTERVAL '26 days'),

('Feedback Submission Interface', 'Design and implement the interface for customers to submit feedback.', 'In Progress', 'High', 2, '00000000-0000-0000-0000-000000000005', CURRENT_TIMESTAMP - INTERVAL '24 days'),

('Feedback Management Dashboard', 'Create an internal dashboard for managing and responding to customer feedback.', 'Not Started', 'Medium', 2, '00000000-0000-0000-0000-000000000005', CURRENT_TIMESTAMP - INTERVAL '23 days'),

('Automated Test Case Generation', 'Develop a system to automatically generate test cases based on code changes.', 'Not Started', 'Medium', 3, '00000000-0000-0000-0000-000000000004', CURRENT_TIMESTAMP - INTERVAL '19 days'),

('Test Execution Engine', 'Build an engine to execute automated tests across different environments.', 'Not Started', 'High', 3, '00000000-0000-0000-0000-000000000004', CURRENT_TIMESTAMP - INTERVAL '18 days'),

('Knowledge Base Structure', 'Define the structure and taxonomy for the knowledge base.', 'Completed', 'High', 4, '00000000-0000-0000-0000-000000000002', CURRENT_TIMESTAMP - INTERVAL '14 days'),

('Content Creation and Migration', 'Create initial content and migrate existing documentation.', 'In Progress', 'Medium', 4, '00000000-0000-0000-0000-000000000002', CURRENT_TIMESTAMP - INTERVAL '13 days'),

('Data Collection and Processing', 'Set up data collection and processing pipelines for the analytics dashboard.', 'Not Started', 'High', 5, '00000000-0000-0000-0000-000000000010', CURRENT_TIMESTAMP - INTERVAL '9 days'),

('AI Model Development', 'Develop and train AI models for predictive analytics.', 'Not Started', 'Medium', 5, '00000000-0000-0000-0000-000000000010', CURRENT_TIMESTAMP - INTERVAL '8 days');
