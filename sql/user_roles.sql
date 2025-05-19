-- Create user_roles association table
CREATE TABLE IF NOT EXISTS user_roles (
    user_id VARCHAR(36) NOT NULL,
    role_id INTEGER NOT NULL,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles (id) ON DELETE CASCADE
);

-- Assign roles to users
-- Admin User
INSERT INTO user_roles (user_id, role_id) VALUES
('00000000-0000-0000-0000-000000000001', 1);

-- John Doe - Developer
INSERT INTO user_roles (user_id, role_id) VALUES
('00000000-0000-0000-0000-000000000002', 2);

-- Jane Smith - Manager and Product Owner
INSERT INTO user_roles (user_id, role_id) VALUES
('00000000-0000-0000-0000-000000000003', 3),
('00000000-0000-0000-0000-000000000003', 5);

-- Bob Johnson - Tester
INSERT INTO user_roles (user_id, role_id) VALUES
('00000000-0000-0000-0000-000000000004', 7);

-- Alice Williams - Viewer
INSERT INTO user_roles (user_id, role_id) VALUES
('00000000-0000-0000-0000-000000000005', 4);

-- Charlie Brown - Scrum Master
INSERT INTO user_roles (user_id, role_id) VALUES
('00000000-0000-0000-0000-000000000006', 6);

-- Diana Miller - Developer
INSERT INTO user_roles (user_id, role_id) VALUES
('00000000-0000-0000-0000-000000000007', 2);

-- Edward Davis - Developer
INSERT INTO user_roles (user_id, role_id) VALUES
('00000000-0000-0000-0000-000000000008', 2);

-- Fiona Garcia - Developer
INSERT INTO user_roles (user_id, role_id) VALUES
('00000000-0000-0000-0000-000000000009', 2);

-- George Wilson - Admin and Manager
INSERT INTO user_roles (user_id, role_id) VALUES
('00000000-0000-0000-0000-000000000010', 1),
('00000000-0000-0000-0000-000000000010', 3);
