-- Create standup_notes table
CREATE TABLE IF NOT EXISTS standup_notes (
    id SERIAL PRIMARY KEY,
    meeting_id INTEGER NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    yesterday_work TEXT,
    today_work TEXT,
    blockers TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (meeting_id) REFERENCES meetings (id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Insert mock standup notes
INSERT INTO standup_notes (meeting_id, user_id, yesterday_work, today_work, blockers, created_at) VALUES
(1, '00000000-0000-0000-0000-000000000002', 'Completed research on authentication libraries. Started implementing login API.', 'Continue working on login API. Start designing biometric authentication flow.', 'None', CURRENT_TIMESTAMP - INTERVAL '1 day'),

(1, '00000000-0000-0000-0000-000000000007', 'Finished login screen design implementation. Started working on form validation.', 'Complete form validation. Start implementing feedback form UI.', 'Waiting for final design approval for the feedback form.', CURRENT_TIMESTAMP - INTERVAL '1 day'),

(1, '00000000-0000-0000-0000-000000000008', 'Worked on database schema for offline storage. Started implementing the storage mechanism.', 'Continue implementing offline storage. Review login API implementation.', 'Need clarification on sync conflict resolution strategy.', CURRENT_TIMESTAMP - INTERVAL '1 day'),

(7, '00000000-0000-0000-0000-000000000002', 'Completed knowledge base category structure. Started documenting the API.', 'Finish API documentation. Start working on search functionality.', 'None', CURRENT_TIMESTAMP - INTERVAL '1 day'),

(7, '00000000-0000-0000-0000-000000000004', 'Tested content migration with sample data. Identified some formatting issues.', 'Fix formatting issues in content migration. Start testing search functionality.', 'Some complex formatting is not being preserved during migration.', CURRENT_TIMESTAMP - INTERVAL '1 day');
