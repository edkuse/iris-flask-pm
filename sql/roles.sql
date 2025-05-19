-- Create roles table
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(255),
    is_system_role BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

-- Insert default roles
INSERT INTO roles (id, name, description, is_system_role, created_at) VALUES
(1, 'admin', 'Administrator with full access to all features', TRUE, CURRENT_TIMESTAMP),
(2, 'developer', 'Developer with access to tasks and code', TRUE, CURRENT_TIMESTAMP),
(3, 'manager', 'Manager with access to planning and reporting', TRUE, CURRENT_TIMESTAMP),
(4, 'viewer', 'Viewer with read-only access', TRUE, CURRENT_TIMESTAMP),
(5, 'product_owner', 'Product owner with access to product backlog and prioritization', FALSE, CURRENT_TIMESTAMP),
(6, 'scrum_master', 'Scrum master with access to sprint planning and facilitation', FALSE, CURRENT_TIMESTAMP),
(7, 'tester', 'Tester with access to testing and quality assurance', FALSE, CURRENT_TIMESTAMP);
