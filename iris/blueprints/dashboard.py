from flask import Blueprint, render_template
from flask_login import current_user, login_required
from iris.models import (
    Epic,
    ProductIdea,
    Sprint,
    StandupMeeting,
    StandupNote,
    StatusEnum,
    Task,
    UserStory
)
from datetime import date

bp = Blueprint('dashboard', __name__)


@bp.route('/')
@login_required
def index():
    # Count items
    product_ideas_count = ProductIdea.query.count()
    epics_count = Epic.query.count()
    user_stories_count = UserStory.query.count()
    tasks_count = Task.query.count()
    
    # Get task status counts
    todo_tasks = Task.query.filter_by(status=StatusEnum.todo).count()
    in_progress_tasks = Task.query.filter_by(status=StatusEnum.in_progress).count()
    review_tasks = Task.query.filter_by(status=StatusEnum.review).count()
    done_tasks = Task.query.filter_by(status=StatusEnum.done).count()

    # Get recent epics
    recent_epics = Epic.query.order_by(Epic.created_at.desc()).limit(3).all()

    # Get current sprint
    current_sprint = Sprint.query.filter_by(status='active').first()
    
    # Sprint metrics
    sprint_story_points = 0
    sprint_completed_points = 0
    sprint_stories_count = 0
    sprint_completion_percentage = 0
    sprint_recent_stories = []

    if current_sprint:
        # Get sprint stories
        sprint_stories = UserStory.query.filter_by(sprint_id=current_sprint.id).all()
        sprint_stories_count = len(sprint_stories)
        
        # Calculate story points
        for story in sprint_stories:
            if story.story_points:
                sprint_story_points += story.story_points
                if story.status == 'done':
                    sprint_completed_points += story.story_points
        
        # Calculate completion percentage
        if sprint_story_points > 0:
            sprint_completion_percentage = int((sprint_completed_points / sprint_story_points) * 100)
        
        # Get recent stories in sprint
        sprint_recent_stories = UserStory.query.filter_by(sprint_id=current_sprint.id).order_by(desc(UserStory.updated_at)).limit(5).all()
    
    # Get today's standup
    today_standup = StandupMeeting.query.filter_by(date=date.today()).first()
    
    # Check if user has submitted update for today's standup
    has_submitted_update = False
    standup_notes = []
    
    if today_standup:
        has_submitted_update = StandupNote.query.filter_by(
            meeting_id=today_standup.id,
            user_id=current_user.id
        ).first() is not None
        
        # Get all notes for today's standup
        standup_notes = StandupNote.query.filter_by(meeting_id=today_standup.id).all()
    
    return render_template(
        'dashboard/index.html',
        product_ideas_count=product_ideas_count,
        epics_count=epics_count,
        user_stories_count=user_stories_count,
        tasks_count=tasks_count,
        todo_tasks=todo_tasks,
        in_progress_tasks=in_progress_tasks,
        review_tasks=review_tasks,
        done_tasks=done_tasks,
        recent_epics=recent_epics,
        current_sprint=current_sprint,
        sprint_story_points=sprint_story_points,
        sprint_completed_points=sprint_completed_points,
        sprint_stories_count=sprint_stories_count,
        sprint_completion_percentage=sprint_completion_percentage,
        sprint_recent_stories=sprint_recent_stories,
        today_standup=today_standup,
        has_submitted_update=has_submitted_update,
        standup_notes=standup_notes
    )
