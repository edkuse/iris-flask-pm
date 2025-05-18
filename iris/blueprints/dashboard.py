from flask import Blueprint, render_template
from flask_login import current_user
from iris.models import ProductIdea, Epic, UserStory, Task, StatusEnum

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
def index():
    """Dashboard home page."""
    # If user is not authenticated, show a landing page
    if not current_user.is_authenticated:
        return render_template('dashboard/landing.html')
    
    # Dashboard overview
    product_ideas_count = ProductIdea.query.count()
    epics_count = Epic.query.count()
    user_stories_count = UserStory.query.count()
    tasks_count = Task.query.count()
    
    # Recent epics
    recent_epics = Epic.query.order_by(Epic.created_at.desc()).limit(3).all()
    
    # Tasks by status
    todo_tasks = Task.query.filter_by(status=StatusEnum.todo).count()
    in_progress_tasks = Task.query.filter_by(status=StatusEnum.in_progress).count()
    review_tasks = Task.query.filter_by(status=StatusEnum.review).count()
    done_tasks = Task.query.filter_by(status=StatusEnum.done).count()
    
    return render_template('index.html', 
                          product_ideas_count=product_ideas_count,
                          epics_count=epics_count,
                          user_stories_count=user_stories_count,
                          tasks_count=tasks_count,
                          recent_epics=recent_epics,
                          todo_tasks=todo_tasks,
                          in_progress_tasks=in_progress_tasks,
                          review_tasks=review_tasks,
                          done_tasks=done_tasks)
