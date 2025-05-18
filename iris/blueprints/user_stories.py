from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from iris.extensions import db
from iris.models import UserStory, Epic, Comment, StatusEnum
from iris.utils import flash_success, flash_error

user_stories_bp = Blueprint('user_stories', __name__)


@user_stories_bp.route('/')
@login_required
def index():
    epic_id = request.args.get('epic_id', type=int)
    
    if epic_id:
        stories = UserStory.query.filter_by(epic_id=epic_id).all()
        epic = Epic.query.get_or_404(epic_id)
        return render_template('user_stories/index.html', stories=stories, epic=epic)
    else:
        stories = UserStory.query.all()
        return render_template('user_stories/index.html', stories=stories, epic=None)


@user_stories_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if request.method == 'POST':
        title = request.form.get('title')
        role = request.form.get('role')
        goal = request.form.get('goal')
        benefit = request.form.get('benefit')
        priority = request.form.get('priority')
        status = StatusEnum[request.form.get('status', 'backlog')]
        epic_id = request.form.get('epic_id')
        
        story = UserStory(
            title=title,
            role=role,
            goal=goal,
            benefit=benefit,
            priority=priority,
            status=status,
            epic_id=epic_id if epic_id else None,
            creator_id=current_user.id
        )
        
        db.session.add(story)
        db.session.commit()
        
        flash_success('User story created successfully!')
        return redirect(url_for('user_stories.index', epic_id=epic_id))
    
    epic_id = request.args.get('epic_id')
    epics = Epic.query.all()
    return render_template('user_stories/new.html', epics=epics, epic_id=epic_id)


@user_stories_bp.route('/<int:story_id>')
@login_required
def view(story_id):
    story = UserStory.query.get_or_404(story_id)
    return render_template('user_stories/view.html', story=story)


@user_stories_bp.route('/<int:story_id>/add-comment', methods=['POST'])
@login_required
def add_comment(story_id):
    story = UserStory.query.get_or_404(story_id)
    content = request.form.get('content')
    
    if content:
        comment = Comment(
            content=content,
            author=current_user.display_name,
            author_id=current_user.id,
            story_id=story_id
        )
        
        db.session.add(comment)
        db.session.commit()
        
        flash_success('Comment added successfully!')

    else:
        flash_error('Comment cannot be empty!')
    
    return redirect(url_for('user_stories.view', story_id=story_id))
