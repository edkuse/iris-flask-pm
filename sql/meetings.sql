-- Create enum types
CREATE TYPE meeting_type AS ENUM ('standup', 'planning', 'review', 'retrospective', 'other');
CREATE TYPE meeting_status AS ENUM ('Scheduled', 'In Progress', 'Completed');
CREATE TYPE retrospective_category AS ENUM ('went_well', 'to_improve', 'action_item');

-- Create standup_meetings table
CREATE TABLE standup_meetings (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    sprint_id INTEGER REFERENCES sprints(id) ON DELETE SET NULL,
    status meeting_status NOT NULL DEFAULT 'Scheduled',
    start_time TIME NOT NULL,
    duration_minutes INTEGER NOT NULL DEFAULT 15,
    meeting_link VARCHAR(255),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE,
    creator_id VARCHAR(36) REFERENCES users(id) ON DELETE SET NULL
);

-- Create standup_notes table
CREATE TABLE standup_notes (
    id SERIAL PRIMARY KEY,
    meeting_id INTEGER NOT NULL REFERENCES standup_meetings(id) ON DELETE CASCADE,
    user_id VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    yesterday TEXT,
    today TEXT,
    blockers TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE
);

-- Create retrospective_meetings table
CREATE TABLE retrospective_meetings (
    id SERIAL PRIMARY KEY,
    sprint_id INTEGER NOT NULL REFERENCES sprints(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    status meeting_status NOT NULL DEFAULT 'Scheduled',
    start_time TIME NOT NULL,
    duration_minutes INTEGER NOT NULL DEFAULT 60,
    meeting_link VARCHAR(255),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE,
    creator_id VARCHAR(36) REFERENCES users(id) ON DELETE SET NULL
);

-- Create retrospective_items table
CREATE TABLE retrospective_items (
    id SERIAL PRIMARY KEY,
    meeting_id INTEGER NOT NULL REFERENCES retrospective_meetings(id) ON DELETE CASCADE,
    user_id VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    category retrospective_category NOT NULL,
    content TEXT NOT NULL,
    votes INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE
);

-- Create action_items table
CREATE TABLE action_items (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    assignee_id VARCHAR(36) REFERENCES users(id) ON DELETE SET NULL,
    due_date DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'open',
    standup_meeting_id INTEGER REFERENCES standup_meetings(id) ON DELETE CASCADE,
    retro_meeting_id INTEGER REFERENCES retrospective_meetings(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE,
    creator_id VARCHAR(36) REFERENCES users(id) ON DELETE SET NULL,
    -- Ensure an action item is linked to either a standup or a retrospective, but not both
    CONSTRAINT action_item_meeting_check CHECK (
        (standup_meeting_id IS NULL AND retro_meeting_id IS NOT NULL) OR
        (standup_meeting_id IS NOT NULL AND retro_meeting_id IS NULL)
    )
);

-- Create indexes for performance
CREATE INDEX idx_standup_meetings_date ON standup_meetings(date);
CREATE INDEX idx_standup_meetings_sprint_id ON standup_meetings(sprint_id);
CREATE INDEX idx_standup_notes_meeting_id ON standup_notes(meeting_id);
CREATE INDEX idx_standup_notes_user_id ON standup_notes(user_id);
CREATE INDEX idx_retrospective_meetings_sprint_id ON retrospective_meetings(sprint_id);
CREATE INDEX idx_retrospective_meetings_date ON retrospective_meetings(date);
CREATE INDEX idx_retrospective_items_meeting_id ON retrospective_items(meeting_id);
CREATE INDEX idx_retrospective_items_user_id ON retrospective_items(user_id);
CREATE INDEX idx_action_items_assignee_id ON action_items(assignee_id);
CREATE INDEX idx_action_items_standup_meeting_id ON action_items(standup_meeting_id);
CREATE INDEX idx_action_items_retro_meeting_id ON action_items(retro_meeting_id);
CREATE INDEX idx_action_items_due_date ON action_items(due_date);
CREATE INDEX idx_action_items_status ON action_items(status);

-- Add triggers for updated_at timestamps
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_standup_meetings_modtime
    BEFORE UPDATE ON standup_meetings
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

CREATE TRIGGER update_standup_notes_modtime
    BEFORE UPDATE ON standup_notes
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

CREATE TRIGGER update_retrospective_meetings_modtime
    BEFORE UPDATE ON retrospective_meetings
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

CREATE TRIGGER update_retrospective_items_modtime
    BEFORE UPDATE ON retrospective_items
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

CREATE TRIGGER update_action_items_modtime
    BEFORE UPDATE ON action_items
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();
