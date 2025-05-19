-- Create retrospective_item_type enum
CREATE TYPE retrospective_item_type AS ENUM ('what_went_well', 'what_could_be_improved', 'action_item');

-- Create retrospective_items table
CREATE TABLE IF NOT EXISTS retrospective_items (
    id SERIAL PRIMARY KEY,
    meeting_id INTEGER NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    item_type retrospective_item_type NOT NULL,
    content TEXT NOT NULL,
    votes INTEGER DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (meeting_id) REFERENCES meetings (id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Insert mock retrospective items
INSERT INTO retrospective_items (meeting_id, user_id, item_type, content, votes, created_at) VALUES
(4, '00000000-0000-0000-0000-000000000002', 'what_went_well', 'The team collaborated effectively on the authentication implementation.', 3, CURRENT_TIMESTAMP - INTERVAL '1 day'),

(4, '00000000-0000-0000-0000-000000000007', 'what_went_well', 'Design handoff process was smooth and designs were clear.', 2, CURRENT_TIMESTAMP - INTERVAL '1 day'),

(4, '00000000-0000-0000-0000-000000000008', 'what_went_well', 'Daily standups were focused and helped identify blockers quickly.', 4, CURRENT_TIMESTAMP - INTERVAL '1 day'),

(4, '00000000-0000-0000-0000-000000000002', 'what_could_be_improved', 'We underestimated the complexity of the offline sync feature.', 5, CURRENT_TIMESTAMP - INTERVAL '1 day'),

(4, '00000000-0000-0000-0000-000000000007', 'what_could_be_improved', 'There were some delays in getting design feedback.', 1, CURRENT_TIMESTAMP - INTERVAL '1 day'),

(4, '00000000-0000-0000-0000-000000000006', 'what_could_be_improved', 'Documentation was not kept up-to-date with implementation changes.', 3, CURRENT_TIMESTAMP - INTERVAL '1 day'),

(4, '00000000-0000-0000-0000-000000000006', 'action_item', 'Implement a process for updating documentation alongside code changes.', 4, CURRENT_TIMESTAMP - INTERVAL '1 day'),

(4, '00000000-0000-0000-0000-000000000002', 'action_item', 'Break down complex features into smaller, more manageable tasks.', 5, CURRENT_TIMESTAMP - INTERVAL '1 day');
