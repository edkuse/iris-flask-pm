from iris import create_app
from iris.extensions import db
from iris.models import ProductIdea, Epic, UserStory, Task, Comment, StatusEnum, User
from datetime import datetime, timedelta


def init_db():
    app = create_app()
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if database is already populated
        if ProductIdea.query.count() > 0:
            print("Database already contains data. Skipping initialization.")
            return
        
        # Create a test user
        test_user = User(
            id="test-user-id",
            email="test@example.com",
            display_name="Test User",
            job_title="Developer",
            department="Engineering"
        )
        db.session.add(test_user)
        db.session.commit()
        
        # Sample data - Product Ideas
        product_ideas = [
            ProductIdea(
                title="Mobile App Redesign",
                description="Redesign the mobile app to improve user experience and increase engagement",
                tags=["UX", "Mobile", "Engagement"],
                problem_statement="Current mobile app has low engagement and high bounce rate",
                success_metrics="Increase user engagement by 30%, reduce bounce rate by 20%",
                impact_level="high",
                creator_id=test_user.id
            ),
            ProductIdea(
                title="API Integration Platform",
                description="Create a platform to easily integrate with third-party APIs",
                tags=["API", "Integration", "Platform"],
                problem_statement="Integrating with third-party APIs is time-consuming and error-prone",
                success_metrics="Reduce integration time by 50%, increase successful integrations by 40%",
                impact_level="medium",
                creator_id=test_user.id
            ),
            ProductIdea(
                title="Customer Feedback System",
                description="Implement a system to collect and analyze customer feedback",
                tags=["Feedback", "Analytics", "Customer"],
                problem_statement="We lack a systematic way to collect and analyze customer feedback",
                success_metrics="Collect feedback from at least 20% of customers, identify top 5 improvement areas",
                impact_level="high",
                creator_id=test_user.id
            )
        ]
        
        db.session.add_all(product_ideas)
        db.session.commit()
        
        # Sample data - Epics
        epics = [
            Epic(
                title="User Authentication Overhaul",
                description="Improve the user authentication system to enhance security and user experience",
                priority="high",
                goal="Implement a more secure and user-friendly authentication system",
                tags=["Security", "UX", "Authentication"],
                status=StatusEnum.in_progress,
                product_idea_id=1,
                creator_id=test_user.id
            ),
            Epic(
                title="Dashboard Redesign",
                description="Redesign the dashboard to provide better insights and improve usability",
                priority="medium",
                goal="Create a more intuitive and informative dashboard",
                tags=["UX", "Dashboard", "Analytics"],
                status=StatusEnum.backlog,
                product_idea_id=1,
                creator_id=test_user.id
            ),
            Epic(
                title="API Gateway Implementation",
                description="Implement an API gateway to manage API requests and improve performance",
                priority="high",
                goal="Create a centralized API gateway for all third-party integrations",
                tags=["API", "Performance", "Integration"],
                status=StatusEnum.backlog,
                product_idea_id=2,
                creator_id=test_user.id
            )
        ]
        
        db.session.add_all(epics)
        db.session.commit()
        
        # Sample data - User Stories
        user_stories = [
            UserStory(
                title="Social Login Integration",
                role="user",
                goal="log in using my social media accounts",
                benefit="I don't have to remember another password",
                priority="high",
                status=StatusEnum.in_progress,
                epic_id=1,
                creator_id=test_user.id
            ),
            UserStory(
                title="Password Reset Flow",
                role="user",
                goal="reset my password easily if I forget it",
                benefit="I can regain access to my account quickly",
                priority="medium",
                status=StatusEnum.backlog,
                epic_id=1,
                creator_id=test_user.id
            ),
            UserStory(
                title="Customizable Dashboard Widgets",
                role="user",
                goal="customize the widgets on my dashboard",
                benefit="I can focus on the information that matters most to me",
                priority="low",
                status=StatusEnum.backlog,
                epic_id=2,
                creator_id=test_user.id
            ),
            UserStory(
                title="API Usage Analytics",
                role="developer",
                goal="view analytics on API usage",
                benefit="I can optimize my API calls and improve performance",
                priority="medium",
                status=StatusEnum.backlog,
                epic_id=3,
                creator_id=test_user.id
            )
        ]
        
        db.session.add_all(user_stories)
        db.session.commit()
        
        # Sample data - Tasks
        tasks = [
            Task(
                title="Implement Google OAuth",
                description="Integrate Google OAuth for user authentication",
                status=StatusEnum.in_progress,
                assignee="John Doe",
                assignee_id=test_user.id,
                effort="Medium",
                due_date=datetime.now() + timedelta(days=5),
                story_id=1,
                creator_id=test_user.id
            ),
            Task(
                title="Implement Facebook OAuth",
                description="Integrate Facebook OAuth for user authentication",
                status=StatusEnum.todo,
                assignee="Jane Smith",
                assignee_id=test_user.id,
                effort="Medium",
                due_date=datetime.now() + timedelta(days=7),
                story_id=1,
                creator_id=test_user.id
            ),
            Task(
                title="Design Password Reset Email",
                description="Create the email template for password reset",
                status=StatusEnum.todo,
                assignee="Alice Johnson",
                assignee_id=test_user.id,
                effort="Small",
                due_date=datetime.now() + timedelta(days=3),
                story_id=2,
                creator_id=test_user.id
            ),
            Task(
                title="Implement Password Reset API",
                description="Create the API endpoint for password reset",
                status=StatusEnum.todo,
                assignee="Bob Brown",
                assignee_id=test_user.id,
                effort="Medium",
                due_date=datetime.now() + timedelta(days=6),
                story_id=2,
                creator_id=test_user.id
            ),
            Task(
                title="Design Widget Configuration UI",
                description="Create the UI for configuring dashboard widgets",
                status=StatusEnum.todo,
                assignee="Charlie Davis",
                assignee_id=test_user.id,
                effort="Large",
                due_date=datetime.now() + timedelta(days=10),
                story_id=3,
                creator_id=test_user.id
            ),
            Task(
                title="Implement API Usage Tracking",
                description="Create a system to track API usage",
                status=StatusEnum.todo,
                assignee="David Wilson",
                assignee_id=test_user.id,
                effort="Large",
                due_date=datetime.now() + timedelta(days=12),
                story_id=4,
                creator_id=test_user.id
            )
        ]
        
        db.session.add_all(tasks)
        db.session.commit()
        
        # Sample data - Comments
        comments = [
            Comment(
                content="I've started working on this. Will update the PR soon.",
                author="John Doe",
                author_id=test_user.id,
                task_id=1
            ),
            Comment(
                content="Need to check if we have the right API credentials for this.",
                author="Jane Smith",
                author_id=test_user.id,
                task_id=2
            ),
            Comment(
                content="Should we include a link to reset the password in the email?",
                author="Alice Johnson",
                author_id=test_user.id,
                task_id=3
            ),
            Comment(
                content="This user story is more complex than we initially thought.",
                author="Charlie Davis",
                author_id=test_user.id,
                story_id=3
            )
        ]
        
        db.session.add_all(comments)
        db.session.commit()
        
        print("Database initialized with sample data.")

if __name__ == "__main__":
    init_db()
