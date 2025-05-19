-- Create tasks table
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) NOT NULL DEFAULT 'To Do',
    priority VARCHAR(50),
    estimated_hours FLOAT,
    actual_hours FLOAT,
    user_story_id INTEGER,
    assignee_id VARCHAR(36),
    creator_id VARCHAR(36) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (user_story_id) REFERENCES user_stories (id) ON DELETE SET NULL,
    FOREIGN KEY (assignee_id) REFERENCES users (id) ON DELETE SET NULL,
    FOREIGN KEY (creator_id) REFERENCES users (id)
);

-- Insert mock tasks
INSERT INTO tasks (title, description, status, priority, estimated_hours, actual_hours, user_story_id, assignee_id, creator_id, created_at) VALUES
('Design login screen', 'Create wireframes and mockups for the login screen.', 'Done', 'High', 4, 3.5, 1, '00000000-0000-0000-0000-000000000005', '00000000-0000-0000-0000-000000000003', CURRENT_TIMESTAMP - INTERVAL '26 days'),

('Implement login API', 'Create backend API for user authentication.', 'In Progress', 'High', 8, NULL, 1, '00000000-0000-0000-0000-000000000008', '00000000-0000-0000-0000-000000000003', CURRENT_TIMESTAMP - INTERVAL '25 days'),

('Implement login UI', 'Develop the frontend login interface according to the design.', 'To Do', 'High', 6, NULL, 1, '00000000-0000-0000-0000-000000000007', '00000000-0000-0000-0000-000000000003', CURRENT_TIMESTAMP - INTERVAL '24 days'),

('Research biometric authentication libraries', 'Evaluate available libraries for biometric authentication on iOS and Android.', 'To Do', 'Medium', 4, NULL, 2, '00000000-0000-0000-0000-000000000002', '00000000-0000-0000-0000-000000000003', CURRENT_TIMESTAMP - INTERVAL '23 days'),

('Design inspection form', 'Create wireframes and mockups for the inspection form.', 'To Do', 'High', 6, NULL, 3, '00000000-0000-0000-0000-000000000005', '00000000-0000-0000-0000-000000000003', CURRENT_TIMESTAMP - INTERVAL '22 days'),

('Implement form validation', 'Add client-side validation for the inspection form.', 'To Do', 'Medium', 4, NULL, 3, '00000000-0000-0000-0000-000000000007', '00000000-0000-0000-0000-000000000003', CURRENT_TIMESTAMP - INTERVAL '21 days'),

('Design offline storage schema', 'Design the database schema for storing forms offline.', 'To Do', 'High', 4, NULL, 4, '00000000-0000-0000-0000-000000000008', '00000000-0000-0000-0000-000000000002', CURRENT_TIMESTAMP - INTERVAL '20 days'),

('Implement offline storage', 'Develop the functionality to store forms offline.', 'To Do', 'High', 8, NULL, 4, '00000000-0000-0000-0000-000000000008', '00000000-0000-0000-0000-000000000002', CURRENT_TIMESTAMP - INTERVAL '19 days'),

('Design feedback form', 'Create wireframes and mockups for the customer feedback form.', 'Done', 'High', 4, 3, 5, '00000000-0000-0000-0000-000000000005', '00000000-0000-0000-0000-000000000005', CURRENT_TIMESTAMP - INTERVAL '22 days'),

('Implement feedback form UI', 'Develop the frontend feedback form according to the design.', 'In Progress', 'High', 6, NULL, 5, '00000000-0000-0000-0000-000000000007', '00000000-0000-0000-0000-000000000005', CURRENT_TIMESTAMP - INTERVAL '21 days'),

('Create knowledge base schema', 'Design the database schema for the knowledge base.', 'Done', 'High', 4, 5, 7, '00000000-0000-0000-0000-000000000008', '00000000-0000-0000-0000-000000000002', CURRENT_TIMESTAMP - INTERVAL '28 days'),

('Implement category management UI', 'Develop the interface for managing knowledge base categories.', 'Done', 'Medium', 6, 7, 7, '00000000-0000-0000-0000-000000000007', '00000000-0000-0000-0000-000000000002', CURRENT_TIMESTAMP - INTERVAL '27 days'),

('Create content import tool', 'Develop a tool to import existing documentation.', 'In Progress', 'Medium', 8, NULL, 8, '00000000-0000-0000-0000-000000000008', '00000000-0000-0000-0000-000000000002', CURRENT_TIMESTAMP - INTERVAL '26 days'),

('Test content migration', 'Test the migration process with sample content.', 'To Do', 'Medium', 4, NULL, 8, '00000000-0000-0000-0000-000000000004', '00000000-0000-0000-0000-000000000002', CURRENT_TIMESTAMP - INTERVAL '25 days');
