-- Create product_ideas table
CREATE TABLE IF NOT EXISTS product_ideas (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    problem_statement TEXT,
    success_metrics TEXT,
    impact_level VARCHAR(50),
    tags TEXT[],
    creator_id VARCHAR(36) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (creator_id) REFERENCES users (id)
);

-- Insert mock product ideas
INSERT INTO product_ideas (title, description, problem_statement, success_metrics, impact_level, tags, creator_id, created_at) VALUES
('Mobile App for Field Workers', 'A mobile application that allows field workers to access and update project information on the go.', 'Field workers currently have to return to the office to update project status, which is inefficient and causes delays.', 'Reduce time spent on administrative tasks by 30%. Increase real-time data accuracy by 50%.', 'High', ARRAY['mobile', 'field-work', 'productivity'], '00000000-0000-0000-0000-000000000003', CURRENT_TIMESTAMP - INTERVAL '30 days'),

('Customer Feedback Portal', 'A portal where customers can submit feedback, report issues, and track the status of their requests.', 'We currently collect customer feedback through various channels, making it difficult to track and prioritize.', 'Increase customer satisfaction score by 15%. Reduce time to resolve customer issues by 25%.', 'Medium', ARRAY['customer', 'feedback', 'portal'], '00000000-0000-0000-0000-000000000005', CURRENT_TIMESTAMP - INTERVAL '25 days'),

('Automated Testing Framework', 'A framework for automating regression testing across our product suite.', 'Manual testing is time-consuming and prone to human error, leading to bugs in production.', 'Reduce QA testing time by 50%. Decrease production bugs by 30%.', 'High', ARRAY['testing', 'automation', 'quality'], '00000000-0000-0000-0000-000000000004', CURRENT_TIMESTAMP - INTERVAL '20 days'),

('Internal Knowledge Base', 'A centralized knowledge base for internal documentation, processes, and best practices.', 'Information is scattered across different tools and repositories, making it hard for team members to find what they need.', 'Reduce onboarding time for new employees by 40%. Increase productivity by 20%.', 'Medium', ARRAY['knowledge', 'documentation', 'internal'], '00000000-0000-0000-0000-000000000002', CURRENT_TIMESTAMP - INTERVAL '15 days'),

('AI-Powered Analytics Dashboard', 'An analytics dashboard that uses AI to provide insights and recommendations based on project data.', 'Project managers spend too much time analyzing data and identifying trends manually.', 'Reduce time spent on data analysis by 60%. Improve decision-making accuracy by 40%.', 'High', ARRAY['analytics', 'ai', 'dashboard'], '00000000-0000-0000-0000-000000000010', CURRENT_TIMESTAMP - INTERVAL '10 days');
