from flask import Blueprint, render_template
from flask_login import login_required
from iris.extensions import db
from iris.models import Epic, UserStory, Task
from sqlalchemy import desc

bp = Blueprint('timeline', __name__, url_prefix='/timeline')


@bp.route('/')
@login_required
def index():
    # Get all epics, user stories, and tasks
    epics = db.session.query(Epic).order_by(desc(Epic.created_at)).all()
    stories = db.session.query(UserStory).order_by(desc(UserStory.created_at)).all()
    tasks = db.session.query(Task).order_by(desc(Task.created_at)).all()
    
    # Create timeline items
    timeline_items = []
    
    # Add epics to timeline
    for epic in epics:
        timeline_items.append({
            'id': f'epic-{epic.id}',
            'type': 'epic',
            'title': epic.title,
            'description': epic.description,
            'status': epic.status,
            'priority': epic.priority,
            'goal': epic.goal,
            'tags': epic.tags,
            'created_at': epic.created_at,
            'updated_at': epic.updated_at,
            'view_url': f'/epics/{epic.id}'
        })
    
    # Add user stories to timeline
    for story in stories:
        timeline_items.append({
            'id': f'story-{story.id}',
            'type': 'story',
            'title': story.title,
            'role': story.role,
            'goal': story.goal,
            'benefit': story.benefit,
            'status': story.status,
            'priority': story.priority,
            'created_at': story.created_at,
            'updated_at': story.updated_at,
            'view_url': f'/user-stories/{story.id}'
        })
    
    # Add tasks to timeline
    for task in tasks:
        timeline_items.append({
            'id': f'task-{task.id}',
            'type': 'task',
            'title': task.title,
            'description': task.description,
            'status': task.status,
            'assignee': task.assignee,
            'effort': task.effort,
            'due_date': task.due_date,
            'created_at': task.created_at,
            'updated_at': task.updated_at,
            'view_url': f'/tasks/{task.id}'
        })
    
    # Sort timeline items by created_at date (newest first)
    timeline_items.sort(key=lambda x: x['created_at'], reverse=True)
    
    return render_template('timeline/index.html', timeline_items=timeline_items)
