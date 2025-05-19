-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    display_name VARCHAR(255) NOT NULL,
    job_title VARCHAR(255),
    department VARCHAR(255),
    profile_picture VARCHAR(1024),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Insert mock users
INSERT INTO users (id, email, display_name, job_title, department, profile_picture, created_at, last_login) VALUES
('00000000-0000-0000-0000-000000000001', 'admin@example.com', 'Admin User', 'System Administrator', 'IT', 'https://randomuser.me/api/portraits/men/1.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('00000000-0000-0000-0000-000000000002', 'john.doe@example.com', 'John Doe', 'Senior Developer', 'Engineering', 'https://randomuser.me/api/portraits/men/2.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('00000000-0000-0000-0000-000000000003', 'jane.smith@example.com', 'Jane Smith', 'Product Manager', 'Product', 'https://randomuser.me/api/portraits/women/3.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('00000000-0000-0000-0000-000000000004', 'bob.johnson@example.com', 'Bob Johnson', 'QA Engineer', 'Quality Assurance', 'https://randomuser.me/api/portraits/men/4.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('00000000-0000-0000-0000-000000000005', 'alice.williams@example.com', 'Alice Williams', 'UX Designer', 'Design', 'https://randomuser.me/api/portraits/women/5.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('00000000-0000-0000-0000-000000000006', 'charlie.brown@example.com', 'Charlie Brown', 'Scrum Master', 'Engineering', 'https://randomuser.me/api/portraits/men/6.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('00000000-0000-0000-0000-000000000007', 'diana.miller@example.com', 'Diana Miller', 'Frontend Developer', 'Engineering', 'https://randomuser.me/api/portraits/women/7.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('00000000-0000-0000-0000-000000000008', 'edward.davis@example.com', 'Edward Davis', 'Backend Developer', 'Engineering', 'https://randomuser.me/api/portraits/men/8.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('00000000-0000-0000-0000-000000000009', 'fiona.garcia@example.com', 'Fiona Garcia', 'DevOps Engineer', 'Operations', 'https://randomuser.me/api/portraits/women/9.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('00000000-0000-0000-0000-000000000010', 'george.wilson@example.com', 'George Wilson', 'CTO', 'Executive', 'https://randomuser.me/api/portraits/men/10.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
