-- Create comments table
CREATE TABLE IF NOT EXISTS comments (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    -- Polymorphic association
    commentable_type VARCHAR(50) NOT NULL,
    commentable_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Create index for polymorphic lookup
CREATE INDEX comments_commentable_idx ON comments (commentable_type, commentable_id);

-- Insert mock comments
INSERT INTO comments (content, user_id, commentable_type, commentable_id, created_at) VALUES
-- Comments on Product Ideas
('This would be a great addition to our product suite. I think we should prioritize this for the next quarter.', '00000000-0000-0000-0000-000000000003', 'product_idea', 1, CURRENT_TIMESTAMP - INTERVAL '29 days'),

('I agree with Jane. This would solve a major pain point for our field workers.', '00000000-0000-0000-0000-000000000010', 'product_idea', 1, CURRENT_TIMESTAMP - INTERVAL '28 days'),

('We should consider integrating this with our existing CRM system.', '00000000-0000-0000-0000-000000000002', 'product_idea', 2, CURRENT_TIMESTAMP - INTERVAL '24 days'),

-- Comments on Epics
('We need to make sure we support both iOS and Android biometric authentication.', '00000000-0000-0000-0000-000000000002', 'epic', 1, CURRENT_TIMESTAMP - INTERVAL '27 days'),

('Let''s also consider accessibility requirements for the authentication flow.', '00000000-0000-0000-0000-000000000005', 'epic', 1, CURRENT_TIMESTAMP - INTERVAL '26 days'),

('We should prioritize the most common form types for the initial release.', '00000000-0000-0000-0000-000000000003', 'epic', 2, CURRENT_TIMESTAMP - INTERVAL '25 days'),

-- Comments on User Stories
('We should add support for password reset in this story.', '00000000-0000-0000-0000-000000000008', 'user_story', 1, CURRENT_TIMESTAMP - INTERVAL '26 days'),

('Good point. I''ll update the acceptance criteria.', '00000000-0000-0000-0000-000000000003', 'user_story', 1, CURRENT_TIMESTAMP - INTERVAL '25 days'),

('We need to ensure this works with slow internet connections as well.', '00000000-0000-0000-0000-000000000002', 'user_story', 4, CURRENT_TIMESTAMP - INTERVAL '23 days'),

-- Comments on Tasks
('I''ve started working on this. The initial design looks promising.', '00000000-0000-0000-0000-000000000005', 'task', 1, CURRENT_TIMESTAMP - INTERVAL '25 days'),

('I''ve completed the design. Please review when you have a chance.', '00000000-0000-0000-0000-000000000005', 'task', 1, CURRENT_TIMESTAMP - INTERVAL '24 days'),

('I''m running into some issues with the API authentication. Could use some help.', '00000000-0000-0000-0000-000000000008', 'task', 2, CURRENT_TIMESTAMP - INTERVAL '23 days'),

('Let me know what issues you''re facing. I can help.', '00000000-0000-0000-0000-000000000002', 'task', 2, CURRENT_TIMESTAMP - INTERVAL '22 days');
