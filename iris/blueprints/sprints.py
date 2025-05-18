from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import login_required
from iris.extensions import db
from iris.models import Sprint, UserStory, SprintStatusEnum, StatusEnum
from iris.utils import flash_error, flash_success
from datetime import datetime, timedelta
import json

bp = Blueprint('sprints', __name__, url_prefix='/sprints')


@bp.route('/')
@login_required
def index():
    sprints = Sprint.query.order_by(Sprint.start_date.desc()).all()
    active_sprint = next((s for s in sprints if s.is_active), None)
    
    # Group sprints by status
    planning_sprints = [s for s in sprints if s.status == SprintStatusEnum.planning]
    active_sprints = [s for s in sprints if s.status == SprintStatusEnum.active]
    completed_sprints = [s for s in sprints if s.status == SprintStatusEnum.completed]
    
    return render_template('sprints/index.html', 
                          planning_sprints=planning_sprints,
                          active_sprints=active_sprints,
                          completed_sprints=completed_sprints,
                          active_sprint=active_sprint)


@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if request.method == 'POST':
        name = request.form.get('name')
        goal = request.form.get('goal')
        start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d')
        end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d')
        
        # Validate dates
        if end_date <= start_date:
            flash_error('End date must be after start date')
            return render_template('sprints/new.html')
        
        sprint = Sprint(
            name=name,
            goal=goal,
            start_date=start_date,
            end_date=end_date,
            status=SprintStatusEnum.planning
        )
        
        db.session.add(sprint)
        db.session.commit()
        
        flash_success(f'Sprint "{name}" created successfully')
        return redirect(url_for('sprints.view', sprint_id=sprint.id))
    
    # Default sprint duration is 2 weeks
    today = datetime.now().date()
    default_start = today + timedelta(days=(0 - today.weekday()) % 7)  # Next Monday
    default_end = default_start + timedelta(days=13)  # Two weeks later
    
    return render_template('sprints/new.html', 
                          default_start=default_start.strftime('%Y-%m-%d'),
                          default_end=default_end.strftime('%Y-%m-%d'))


@bp.route('/<int:sprint_id>')
@login_required
def view(sprint_id):
    sprint = Sprint.query.get_or_404(sprint_id)
    stories = UserStory.query.filter_by(sprint_id=sprint_id).all()
    
    # Group stories by status
    backlog_stories = [s for s in stories if s.status == StatusEnum.backlog]
    in_progress_stories = [s for s in stories if s.status == StatusEnum.in_progress]
    done_stories = [s for s in stories if s.status == StatusEnum.done]
    
    # Calculate burndown data
    burndown_data = calculate_burndown_data(sprint, stories)
    
    return render_template('sprints/view.html', 
                          sprint=sprint,
                          backlog_stories=backlog_stories,
                          in_progress_stories=in_progress_stories,
                          done_stories=done_stories,
                          burndown_data=json.dumps(burndown_data))


@bp.route('/<int:sprint_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(sprint_id):
    sprint = Sprint.query.get_or_404(sprint_id)
    
    if request.method == 'POST':
        sprint.name = request.form.get('name')
        sprint.goal = request.form.get('goal')
        sprint.start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d')
        sprint.end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d')
        sprint.status = request.form.get('status')
        
        # Validate dates
        if sprint.end_date <= sprint.start_date:
            flash_error('End date must be after start date')
            return render_template('sprints/edit.html', sprint=sprint)
        
        db.session.commit()
        
        flash_success(f'Sprint "{sprint.name}" updated successfully')
        return redirect(url_for('sprints.view', sprint_id=sprint.id))
    
    return render_template('sprints/edit.html', sprint=sprint)


@bp.route('/<int:sprint_id>/delete', methods=['POST'])
@login_required
def delete(sprint_id):
    sprint = Sprint.query.get_or_404(sprint_id)
    
    # Remove sprint association from user stories
    for story in sprint.user_stories:
        story.sprint_id = None
    
    db.session.delete(sprint)
    db.session.commit()
    
    flash_success(f'Sprint "{sprint.name}" deleted successfully')
    return redirect(url_for('sprints.index'))


@bp.route('/<int:sprint_id>/planning')
@login_required
def planning(sprint_id):
    sprint = Sprint.query.get_or_404(sprint_id)
    
    # Get stories already in the sprint
    sprint_stories = UserStory.query.filter_by(sprint_id=sprint_id).all()
    
    # Get available stories (in backlog, not assigned to any sprint)
    available_stories = UserStory.query.filter_by(sprint_id=None).all()
    
    return render_template('sprints/planning.html', 
                          sprint=sprint,
                          sprint_stories=sprint_stories,
                          available_stories=available_stories)


@bp.route('/<int:sprint_id>/add_story/<int:story_id>', methods=['POST'])
@login_required
def add_story(sprint_id, story_id):
    sprint = Sprint.query.get_or_404(sprint_id)
    story = UserStory.query.get_or_404(story_id)
    
    story.sprint_id = sprint_id
    story_points = request.form.get('story_points')
    if story_points:
        story.story_points = int(story_points)
    
    db.session.commit()
    
    flash_success(f'Story "{story.title}" added to sprint')
    return redirect(url_for('sprints.planning', sprint_id=sprint_id))


@bp.route('/<int:sprint_id>/remove_story/<int:story_id>', methods=['POST'])
@login_required
def remove_story(sprint_id, story_id):
    story = UserStory.query.get_or_404(story_id)
    
    if story.sprint_id == sprint_id:
        story.sprint_id = None
        db.session.commit()
        flash_success(f'Story "{story.title}" removed from sprint')

    else:
        flash_error(f'Story "{story.title}" is not in this sprint')
    
    return redirect(url_for('sprints.planning', sprint_id=sprint_id))


@bp.route('/<int:sprint_id>/start', methods=['POST'])
@login_required
def start_sprint(sprint_id):
    sprint = Sprint.query.get_or_404(sprint_id)
    
    if sprint.status != SprintStatusEnum.planning:
        flash_error('Only sprints in planning status can be started')
        return redirect(url_for('sprints.view', sprint_id=sprint_id))
    
    # Check if there's already an active sprint
    active_sprint = Sprint.query.filter_by(status=SprintStatusEnum.active).first()
    if active_sprint:
        flash_error(f'Cannot start sprint. Sprint "{active_sprint.name}" is already active')
        return redirect(url_for('sprints.view', sprint_id=sprint_id))
    
    sprint.status = SprintStatusEnum.active
    db.session.commit()
    
    flash_success(f'Sprint "{sprint.name}" started successfully')
    return redirect(url_for('sprints.view', sprint_id=sprint_id))


@bp.route('/<int:sprint_id>/complete', methods=['POST'])
@login_required
def complete_sprint(sprint_id):
    sprint = Sprint.query.get_or_404(sprint_id)
    
    if sprint.status != SprintStatusEnum.active:
        flash_error('Only active sprints can be completed')
        return redirect(url_for('sprints.view', sprint_id=sprint_id))
    
    sprint.status = SprintStatusEnum.completed
    
    # Move incomplete stories back to backlog
    for story in sprint.user_stories:
        if story.status != StatusEnum.done:
            story.status = StatusEnum.backlog
            story.sprint_id = None
    
    db.session.commit()
    
    flash_success(f'Sprint "{sprint.name}" completed successfully')
    return redirect(url_for('sprints.view', sprint_id=sprint_id))


@bp.route('/<int:sprint_id>/burndown')
@login_required
def burndown(sprint_id):
    sprint = Sprint.query.get_or_404(sprint_id)
    stories = UserStory.query.filter_by(sprint_id=sprint_id).all()
    
    burndown_data = calculate_burndown_data(sprint, stories)
    
    return render_template('sprints/burndown.html', 
                          sprint=sprint,
                          burndown_data=json.dumps(burndown_data))


def calculate_burndown_data(sprint, stories):
    """Calculate burndown chart data for a sprint"""
    if not sprint.start_date or not sprint.end_date:
        return []
    
    total_points = sum(story.story_points or 0 for story in stories)
    
    # Create a list of dates from start to end
    current_date = sprint.start_date.date()
    end_date = sprint.end_date.date()
    dates = []
    
    while current_date <= end_date:
        dates.append(current_date)
        current_date += timedelta(days=1)
    
    # Ideal burndown - straight line from total points to 0
    ideal_burndown = []
    for i, date in enumerate(dates):
        ideal_points = total_points * (1 - i / (len(dates) - 1)) if len(dates) > 1 else 0
        ideal_burndown.append({
            'date': date.strftime('%Y-%m-%d'),
            'points': round(ideal_points, 1)
        })
    
    # Actual burndown - based on story completion dates
    # For simplicity, we'll just use the current state
    # In a real app, you'd track daily completion
    actual_burndown = []
    remaining_points = total_points
    
    for date in dates:
        # If date is in the future, we don't have actual data
        if date > datetime.now().date():
            break
            
        # For past dates, calculate remaining points
        # This is simplified - in a real app, you'd track daily completion
        if date == datetime.now().date():
            remaining_points = total_points - sum((story.story_points or 0) for story in stories if story.status == StatusEnum.done)
            
        actual_burndown.append({
            'date': date.strftime('%Y-%m-%d'),
            'points': remaining_points
        })
    
    return {
        'ideal': ideal_burndown,
        'actual': actual_burndown,
        'total_points': total_points,
        'dates': [date.strftime('%Y-%m-%d') for date in dates]
    }
