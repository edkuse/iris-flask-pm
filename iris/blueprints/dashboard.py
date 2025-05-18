from flask import Blueprint, render_template
from flask_login import current_user
from iris.models import ProductIdea, Epic, UserStory, Sprint, Task, StatusEnum
from datetime import datetime

bp = Blueprint('dashboard', __name__)


@bp.route('/')
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

    # Get current sprint
    current_sprint = Sprint.query.filter(
        Sprint.start_date <= datetime.utcnow(),
        Sprint.end_date >= datetime.utcnow(),
        Sprint.status == 'active'
    ).first()
    
    # If no active sprint, get the next planned sprint
    if not current_sprint:
        current_sprint = Sprint.query.filter(
            Sprint.start_date > datetime.utcnow(),
            Sprint.status == 'planning'
        ).order_by(Sprint.start_date).first()
    
    # Calculate sprint progress if there's an active sprint
    sprint_progress = 0
    if current_sprint and current_sprint.status == 'active':
        total_days = (current_sprint.end_date - current_sprint.start_date).days
        days_passed = (datetime.utcnow() - current_sprint.start_date).days
        sprint_progress = min(100, int((days_passed / total_days) * 100)) if total_days > 0 else 0
    
    # Get sprint stories and completion percentage
    sprint_stories = []
    completion_percentage = 0
    if current_sprint:
        sprint_stories = UserStory.query.filter_by(sprint_id=current_sprint.id).all()
        completed_stories = sum(1 for story in sprint_stories if story.status == 'done')
        completion_percentage = int((completed_stories / len(sprint_stories)) * 100) if sprint_stories else 0
    
    return render_template(
        'dashboard/index.html', 
        product_ideas_count=product_ideas_count,
        epics_count=epics_count,
        user_stories_count=user_stories_count,
        tasks_count=tasks_count,
        recent_epics=recent_epics,
        todo_tasks=todo_tasks,
        in_progress_tasks=in_progress_tasks,
        review_tasks=review_tasks,
        done_tasks=done_tasks,
        current_sprint=current_sprint,
        sprint_progress=sprint_progress,
        sprint_stories=sprint_stories,
        completion_percentage=completion_percentage
    )
