from flask import Blueprint, render_template, request
from iris.extensions import db
from iris.models import Task, UserStory, Epic

kanban_bp = Blueprint('kanban', __name__)


@kanban_bp.route('/')
def index():
    epic_id = request.args.get('epic_id', type=int)
    assignee = request.args.get('assignee')
    
    query = Task.query
    
    if epic_id:
        # Join with UserStory to filter by epic_id
        query = query.join(UserStory).filter(UserStory.epic_id == epic_id)
    
    if assignee:
        query = query.filter(Task.assignee == assignee)
    
    tasks = query.all()
    
    # Get unique assignees for filter dropdown
    assignees = db.session.query(Task.assignee).distinct().filter(Task.assignee != None).all()
    assignees = [a[0] for a in assignees]
    
    # Get epics for filter dropdown
    epics = Epic.query.all()
    
    return render_template('kanban/index.html', tasks=tasks, assignees=assignees, epics=epics)
