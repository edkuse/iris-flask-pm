from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from iris.extensions import db
from iris.models import Comment, Task, UserStory, StatusEnum
from iris.utils.flash import flash_error, flash_success
from datetime import datetime

bp = Blueprint('tasks', __name__, url_prefix='/tasks')


@bp.route('/')
def index():
    story_id = request.args.get('story_id', type=int)
    
    if story_id:
        tasks = Task.query.filter_by(story_id=story_id).all()
        story = UserStory.query.get_or_404(story_id)
        return render_template('tasks/index.html', tasks=tasks, story=story)
    
    else:
        tasks = Task.query.all()
        return render_template('tasks/index.html', tasks=tasks, story=None)


@bp.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        status = StatusEnum[request.form.get('status', 'todo')]
        assignee = request.form.get('assignee')
        effort = request.form.get('effort')
        due_date_str = request.form.get('due_date')
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d') if due_date_str else None
        story_id = request.form.get('story_id')
        
        task = Task(
            title=title,
            description=description,
            status=status,
            assignee=assignee,
            effort=effort,
            due_date=due_date,
            story_id=story_id
        )
        
        db.session.add(task)
        db.session.commit()
        
        flash_success('Task created successfully!')
        return redirect(url_for('tasks.index', story_id=story_id))
    
    story_id = request.args.get('story_id')
    stories = UserStory.query.all()

    return render_template('tasks/new.html', stories=stories, story_id=story_id)


@bp.route('/<int:task_id>')
@login_required
def view(task_id):
    task = Task.query.get_or_404(task_id)
    comments = Comment.query.filter_by(task_id=task_id).order_by(Comment.created_at).all()
    
    return render_template('tasks/view.html', task=task, comments=comments)

@bp.route('/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(task_id):
    task = Task.query.get_or_404(task_id)
    
    if request.method == 'POST':
        task.title = request.form.get('title')
        task.description = request.form.get('description')
        task.status = request.form.get('status')
        task.assignee = request.form.get('assignee')
        task.effort = request.form.get('effort')
        
        due_date_str = request.form.get('due_date')

        if due_date_str:
            try:
                task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d')

            except ValueError:
                flash_error('Invalid date format. Please use YYYY-MM-DD.')
                return redirect(url_for('tasks.edit', task_id=task_id))
            
        else:
            task.due_date = None
        
        db.session.commit()
        
        flash_success('Task updated successfully!')

        return redirect(url_for('tasks.view', task_id=task_id))
    
    return render_template('tasks/edit.html', task=task)


@bp.route('/<int:task_id>/update-status', methods=['POST'])
@login_required
def update_status(task_id):
    task = Task.query.get_or_404(task_id)
    
    status = request.form.get('status')
    if status in ['todo', 'in_progress', 'done']:
        task.status = status
        db.session.commit()

        flash_success('Task status updated successfully!')

    else:
        flash_error('Invalid status value.')
    
    return redirect(url_for('tasks.view', task_id=task_id))


@bp.route('/<int:task_id>/add-comment', methods=['POST'])
@login_required
def add_comment(task_id):
    task = Task.query.get_or_404(task_id)
    
    content = request.form.get('content')
    if not content:
        flash_error('Comment cannot be empty.')
        return redirect(url_for('tasks.view', task_id=task_id))
    
    comment = Comment(
        content=content,
        author=current_user.name,
        task_id=task_id
    )
    
    db.session.add(comment)
    db.session.commit()
    
    flash_success('Comment added successfully!')
    return redirect(url_for('tasks.view', task_id=task_id))


@bp.route('/<int:task_id>/delete', methods=['POST'])
@login_required
def delete(task_id):
    task = Task.query.get_or_404(task_id)
    story_id = task.story_id
    
    db.session.delete(task)
    db.session.commit()
    
    flash_success('Task deleted successfully!')
    return redirect(url_for('user_stories.view', story_id=story_id))
