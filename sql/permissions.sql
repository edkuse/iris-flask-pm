-- Create permissions table
CREATE TABLE IF NOT EXISTS permissions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description VARCHAR(255),
    resource VARCHAR(50) NOT NULL,
    action VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Insert permissions for each resource and action
INSERT INTO permissions (name, description, resource, action, created_at) VALUES
-- Product Idea permissions
('product_idea.create', 'Can create product ideas', 'product_idea', 'create', CURRENT_TIMESTAMP),
('product_idea.read', 'Can view product ideas', 'product_idea', 'read', CURRENT_TIMESTAMP),
('product_idea.update', 'Can update product ideas', 'product_idea', 'update', CURRENT_TIMESTAMP),
('product_idea.delete', 'Can delete product ideas', 'product_idea', 'delete', CURRENT_TIMESTAMP),

-- Epic permissions
('epic.create', 'Can create epics', 'epic', 'create', CURRENT_TIMESTAMP),
('epic.read', 'Can view epics', 'epic', 'read', CURRENT_TIMESTAMP),
('epic.update', 'Can update epics', 'epic', 'update', CURRENT_TIMESTAMP),
('epic.delete', 'Can delete epics', 'epic', 'delete', CURRENT_TIMESTAMP),

-- User Story permissions
('user_story.create', 'Can create user stories', 'user_story', 'create', CURRENT_TIMESTAMP),
('user_story.read', 'Can view user stories', 'user_story', 'read', CURRENT_TIMESTAMP),
('user_story.update', 'Can update user stories', 'user_story', 'update', CURRENT_TIMESTAMP),
('user_story.delete', 'Can delete user stories', 'user_story', 'delete', CURRENT_TIMESTAMP),

-- Task permissions
('task.create', 'Can create tasks', 'task', 'create', CURRENT_TIMESTAMP),
('task.read', 'Can view tasks', 'task', 'read', CURRENT_TIMESTAMP),
('task.update', 'Can update tasks', 'task', 'update', CURRENT_TIMESTAMP),
('task.delete', 'Can delete tasks', 'task', 'delete', CURRENT_TIMESTAMP),

-- Sprint permissions
('sprint.create', 'Can create sprints', 'sprint', 'create', CURRENT_TIMESTAMP),
('sprint.read', 'Can view sprints', 'sprint', 'read', CURRENT_TIMESTAMP),
('sprint.update', 'Can update sprints', 'sprint', 'update', CURRENT_TIMESTAMP),
('sprint.delete', 'Can delete sprints', 'sprint', 'delete', CURRENT_TIMESTAMP),

-- Meeting permissions
('meeting.create', 'Can create meetings', 'meeting', 'create', CURRENT_TIMESTAMP),
('meeting.read', 'Can view meetings', 'meeting', 'read', CURRENT_TIMESTAMP),
('meeting.update', 'Can update meetings', 'meeting', 'update', CURRENT_TIMESTAMP),
('meeting.delete', 'Can delete meetings', 'meeting', 'delete', CURRENT_TIMESTAMP),

-- Comment permissions
('comment.create', 'Can create comments', 'comment', 'create', CURRENT_TIMESTAMP),
('comment.read', 'Can view comments', 'comment', 'read', CURRENT_TIMESTAMP),
('comment.update', 'Can update comments', 'comment', 'update', CURRENT_TIMESTAMP),
('comment.delete', 'Can delete comments', 'comment', 'delete', CURRENT_TIMESTAMP),

-- User permissions
('user.create', 'Can create users', 'user', 'create', CURRENT_TIMESTAMP),
('user.read', 'Can view users', 'user', 'read', CURRENT_TIMESTAMP),
('user.update', 'Can update users', 'user', 'update', CURRENT_TIMESTAMP),
('user.delete', 'Can delete users', 'user', 'delete', CURRENT_TIMESTAMP),

-- Role permissions
('role.create', 'Can create roles', 'role', 'create', CURRENT_TIMESTAMP),
('role.read', 'Can view roles', 'role', 'read', CURRENT_TIMESTAMP),
('role.update', 'Can update roles', 'role', 'update', CURRENT_TIMESTAMP),
('role.delete', 'Can delete roles', 'role', 'delete', CURRENT_TIMESTAMP);
