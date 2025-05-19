-- Create user_stories table
CREATE TABLE IF NOT EXISTS user_stories (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    acceptance_criteria TEXT,
    status VARCHAR(50) NOT NULL DEFAULT 'Backlog',
    priority VARCHAR(50),
    points INTEGER,
    epic_id INTEGER,
    sprint_id INTEGER,
    creator_id VARCHAR(36) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (epic_id) REFERENCES epics (id) ON DELETE SET NULL,
    FOREIGN KEY (sprint_id) REFERENCES sprints (id) ON DELETE SET NULL,
    FOREIGN KEY (creator_id) REFERENCES users (id)
);

-- Insert mock user stories
INSERT INTO user_stories (title, description, acceptance_criteria, status, priority, points, epic_id, sprint_id, creator_id, created_at) VALUES
('User Login with Email', 'As a field worker, I want to log in with my email and password so that I can access the app securely.', '- User can enter email and password\n- System validates credentials\n- User is logged in successfully\n- Error messages are shown for invalid credentials', 'In Progress', 'High', 5, 1, 1, '00000000-0000-0000-0000-000000000003', CURRENT_TIMESTAMP - INTERVAL '27 days'),

('Biometric Authentication', 'As a field worker, I want to use fingerprint or face recognition to log in quickly.', '- User can enable biometric login\n- User can log in using fingerprint or face recognition\n- Fallback to password is available', 'Backlog', 'Medium', 8, 1, 1, '00000000-0000-0000-0000-000000000003', CURRENT_TIMESTAMP - INTERVAL '26 days'),

('Create Inspection Form', 'As a field worker, I want to fill out an inspection form so that I can document site conditions.', '- Form includes all required fields\n- Form can be saved as draft\n- Form can be submitted\n- Validation prevents submission of incomplete forms', 'Backlog', 'High', 13, 2, 2, '00000000-0000-0000-0000-000000000003', CURRENT_TIMESTAMP - INTERVAL '25 days'),

('Offline Form Submission', 'As a field worker, I want to submit forms while offline so that I can work in areas with poor connectivity.', '- Forms can be filled out offline\n- Forms are stored locally\n- Forms are automatically synced when connectivity is restored\n- User is notified of sync status', 'Backlog', 'High', 13, 3, 3, '00000000-0000-0000-0000-000000000002', CURRENT_TIMESTAMP - INTERVAL '24 days'),

('Submit Feedback Form', 'As a customer, I want to submit feedback through a form so that I can share my experience.', '- Form includes rating scale\n- Form includes free text field\n- Form can be submitted\n- Confirmation is shown after submission', 'In Progress', 'High', 5, 4, 4, '00000000-0000-0000-0000-000000000005', CURRENT_TIMESTAMP - INTERVAL '23 days'),

('View Feedback Status', 'As a customer, I want to see the status of my feedback so that I know if it has been addressed.', '- Customer can view all submitted feedback\n- Status is clearly displayed\n- Updates are shown in real-time', 'Backlog', 'Medium', 8, 4, 4, '00000000-0000-0000-0000-000000000005', CURRENT_TIMESTAMP - INTERVAL '22 days'),

('Create Knowledge Base Categories', 'As an admin, I want to create categories for the knowledge base so that content is organized logically.', '- Admin can create, edit, and delete categories\n- Categories can be nested\n- Categories are displayed in a hierarchical structure', 'Done', 'High', 5, 8, 5, '00000000-0000-0000-0000-000000000002', CURRENT_TIMESTAMP - INTERVAL '29 days'),

('Migrate Existing Documentation', 'As a content manager, I want to migrate existing documentation to the knowledge base so that all information is centralized.', '- Content can be imported from various sources\n- Formatting is preserved\n- Content is properly categorized\n- Links are updated to point to the new location', 'In Progress', 'Medium', 13, 9, 5, '00000000-0000-0000-0000-000000000002', CURRENT_TIMESTAMP - INTERVAL '28 days');
