from flask import Blueprint, request
from iris.extensions import db
from iris.models import UserStory, Task, StatusEnum

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/user-stories/<int:story_id>', methods=['PATCH'])
def update_user_story_status(story_id):
    story = UserStory.query.get_or_404(story_id)
    data = request.json
    
    if 'status' in data:
        try:
            story.status = StatusEnum[data['status']]
            db.session.commit()
            return {'success': True}
        
        except (KeyError, ValueError):
            return {'success': False, 'error': 'Invalid status'}, 400
    
    return {'success': False, 'error': 'No status provided'}, 400


@bp.route('/tasks/<int:task_id>', methods=['PATCH'])
def update_task_status(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.json
    
    if 'status' in data:
        try:
            task.status = StatusEnum[data['status']]
            db.session.commit()
            return {'success': True}
        except (KeyError, ValueError):
            return {'success': False, 'error': 'Invalid status'}, 400
    
    return {'success': False, 'error': 'No status provided'}, 400
