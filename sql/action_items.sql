-- Create action_items table
CREATE TABLE IF NOT EXISTS action_items (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) NOT NULL DEFAULT 'Open',
    due_date DATE,
    meeting_id INTEGER,
    assignee_id VARCHAR(36),
    creator_id VARCHAR(36) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (meeting_id) REFERENCES meetings (id) ON DELETE SET NULL,
    FOREIGN KEY (assignee_id) REFERENCES users (id) ON DELETE SET NULL,
    FOREIGN KEY (creator_id) REFERENCES users (id)
);

-- Insert mock action items
INSERT INTO action_items (title, description, status, due_date, meeting_id, assignee_id, creator_id, created_at) VALUES
('Finalize authentication strategy', 'Document and get approval for the authentication strategy, including biometric options.', 'Open', CURRENT_DATE + INTERVAL '3 days', 2, '00000000-0000-0000-0000-000000000002', '00000000-0000-0000-0000-000000000006', CURRENT_TIMESTAMP - INTERVAL '14 days'),

('Create test plan for offline sync', 'Develop a comprehensive test plan for testing offline data synchronization.', 'Open', CURRENT_DATE + INTERVAL '5 days', 2, '00000000-0000-0000-0000-000000000004', '00000000-0000-0000-0000-000000000006', CURRENT_TIMESTAMP - INTERVAL '14 days'),

('Research third-party libraries for forms', 'Research and recommend libraries for handling complex forms in the mobile app.', 'Completed', CURRENT_DATE - INTERVAL '5 days', 2, '00000000-0000-0000-0000-000000000007', '00000000-0000-0000-0000-000000000006', CURRENT_TIMESTAMP - INTERVAL '14 days'),

('Document knowledge base structure', 'Create documentation for the knowledge base structure and taxonomy.', 'Completed', CURRENT_DATE - INTERVAL '10 days', 6, '00000000-0000-0000-0000-000000000002', '00000000-0000-0000-0000-000000000003', CURRENT_TIMESTAMP - INTERVAL '30 days'),

('Set up automated content validation', 'Implement automated validation for content being migrated to the knowledge base.', 'Open', CURRENT_DATE + INTERVAL '2 days', 6, '00000000-0000-0000-0000-000000000004', '00000000-0000-0000-0000-000000000003', CURRENT_TIMESTAMP - INTERVAL '30 days');
