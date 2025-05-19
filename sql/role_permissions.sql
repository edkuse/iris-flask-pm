-- Create role_permissions association table
CREATE TABLE IF NOT EXISTS role_permissions (
    role_id INTEGER NOT NULL,
    permission_id INTEGER NOT NULL,
    PRIMARY KEY (role_id, permission_id),
    FOREIGN KEY (role_id) REFERENCES roles (id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES permissions (id) ON DELETE CASCADE
);

-- Admin role gets all permissions
INSERT INTO role_permissions (role_id, permission_id)
SELECT 1, id FROM permissions;

-- Developer permissions
INSERT INTO role_permissions (role_id, permission_id)
SELECT 2, id FROM permissions 
WHERE (resource IN ('task', 'user_story', 'comment') AND action IN ('create', 'read', 'update', 'delete'))
   OR (resource IN ('product_idea', 'epic', 'sprint', 'meeting') AND action IN ('read', 'update'))
   OR (resource = 'user' AND action = 'read');

-- Manager permissions
INSERT INTO role_permissions (role_id, permission_id)
SELECT 3, id FROM permissions 
WHERE (resource IN ('product_idea', 'epic', 'sprint', 'meeting') AND action IN ('create', 'read', 'update', 'delete'))
   OR (resource IN ('task', 'user_story', 'comment') AND action IN ('read', 'update'))
   OR (resource = 'user' AND action = 'read');

-- Viewer permissions
INSERT INTO role_permissions (role_id, permission_id)
SELECT 4, id FROM permissions 
WHERE action = 'read';

-- Product Owner permissions
INSERT INTO role_permissions (role_id, permission_id)
SELECT 5, id FROM permissions 
WHERE (resource IN ('product_idea', 'epic') AND action IN ('create', 'read', 'update', 'delete'))
   OR (resource IN ('user_story', 'sprint') AND action IN ('create', 'read', 'update'))
   OR (resource IN ('task', 'meeting', 'comment') AND action IN ('read', 'create'))
   OR (resource = 'user' AND action = 'read');

-- Scrum Master permissions
INSERT INTO role_permissions (role_id, permission_id)
SELECT 6, id FROM permissions 
WHERE (resource IN ('sprint', 'meeting') AND action IN ('create', 'read', 'update', 'delete'))
   OR (resource IN ('user_story', 'task', 'comment') AND action IN ('read', 'update'))
   OR (resource IN ('product_idea', 'epic') AND action = 'read')
   OR (resource = 'user' AND action = 'read');

-- Tester permissions
INSERT INTO role_permissions (role_id, permission_id)
SELECT 7, id FROM permissions 
WHERE (resource IN ('task') AND action IN ('read', 'update'))
   OR (resource IN ('user_story', 'epic', 'product_idea', 'sprint', 'meeting') AND action = 'read')
   OR (resource IN ('comment') AND action IN ('read', 'create'))
   OR (resource = 'user' AND action = 'read');
