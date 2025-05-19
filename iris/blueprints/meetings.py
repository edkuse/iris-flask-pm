from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from iris.extensions import db
from iris.models import (
    StandupMeeting, StandupNote, RetrospectiveMeeting, RetrospectiveItem, 
    ActionItem, User, Sprint, RetrospectiveCategory
)
from iris.utils.flash import flash_error, flash_success
from datetime import datetime, date, timedelta
from sqlalchemy import desc

bp = Blueprint('meetings', __name__, url_prefix='/meetings')


# Main meetings index
@bp.route('/')
@login_required
def index():
    # Get upcoming meetings
    today = date.today()
    upcoming_standups = StandupMeeting.query.filter(
        StandupMeeting.date >= today
    ).order_by(StandupMeeting.date, StandupMeeting.start_time).limit(5).all()
    
    upcoming_retros = RetrospectiveMeeting.query.filter(
        RetrospectiveMeeting.date >= today
    ).order_by(RetrospectiveMeeting.date, RetrospectiveMeeting.start_time).limit(5).all()
    
    # Get recent meetings
    recent_standups = StandupMeeting.query.filter(
        StandupMeeting.date < today
    ).order_by(desc(StandupMeeting.date), desc(StandupMeeting.start_time)).limit(5).all()
    
    recent_retros = RetrospectiveMeeting.query.filter(
        RetrospectiveMeeting.date < today
    ).order_by(desc(RetrospectiveMeeting.date), desc(RetrospectiveMeeting.start_time)).limit(5).all()
    
    # Get action items assigned to current user
    my_action_items = ActionItem.query.filter_by(
        assignee_id=current_user.id, 
        status='open'
    ).order_by(ActionItem.due_date).all()
    
    return render_template(
        'meetings/index.html',
        upcoming_standups=upcoming_standups,
        upcoming_retros=upcoming_retros,
        recent_standups=recent_standups,
        recent_retros=recent_retros,
        my_action_items=my_action_items
    )


# Standup routes
@bp.route('/standups/')
@login_required
def standups():
    # Get all standups, ordered by date (newest first)
    standups = StandupMeeting.query.order_by(desc(StandupMeeting.date)).all()
    
    # Get today's standup if it exists
    today = date.today()
    today_standup = StandupMeeting.query.filter_by(date=today).first()
    
    # Check if current user has submitted update for today's standup
    has_submitted = False
    if today_standup:
        has_submitted = StandupNote.query.filter_by(
            meeting_id=today_standup.id,
            user_id=current_user.id
        ).first() is not None
    
    return render_template(
        'meetings/standup/index.html',
        standups=standups,
        today_standup=today_standup,
        has_submitted=has_submitted
    )


@bp.route('/standups/new', methods=['GET', 'POST'])
@login_required
def new_standup():
    if request.method == 'POST':
        # Get form data
        standup_date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        start_time_str = request.form['start_time']
        start_time = datetime.strptime(start_time_str, '%H:%M').time()
        duration = int(request.form['duration'])
        sprint_id = request.form.get('sprint_id')
        meeting_link = request.form.get('meeting_link', '')
        
        # Check if a standup already exists for this date
        existing_standup = StandupMeeting.query.filter_by(date=standup_date).first()
        if existing_standup:
            flash_error('A standup meeting already exists for this date.')
            return redirect(url_for('meetings.standups'))
        
        # Create new standup
        standup = StandupMeeting(
            date=standup_date,
            start_time=start_time,
            duration_minutes=duration,
            sprint_id=sprint_id if sprint_id else None,
            meeting_link=meeting_link
        )
        
        db.session.add(standup)
        db.session.commit()
        
        flash_success('Standup meeting created successfully.')
        return redirect(url_for('meetings.standups'))
    
    # GET request - show form
    sprints = Sprint.query.filter_by(status='active').all()
    return render_template('meetings/standup/new.html', sprints=sprints)


@bp.route('/standups/<int:standup_id>')
@login_required
def view_standup(standup_id):
    standup = StandupMeeting.query.get_or_404(standup_id)
    notes = StandupNote.query.filter_by(meeting_id=standup_id).all()
    action_items = ActionItem.query.filter_by(standup_meeting_id=standup_id).all()
    
    # Get all users
    users = User.query.all()
    
    # Check which users have submitted updates
    submitted_user_ids = [note.user_id for note in notes]
    
    return render_template(
        'meetings/standup/view.html',
        standup=standup,
        notes=notes,
        action_items=action_items,
        users=users,
        submitted_user_ids=submitted_user_ids
    )


@bp.route('/standups/<int:standup_id>/submit', methods=['GET', 'POST'])
@login_required
def submit_standup(standup_id):
    standup = StandupMeeting.query.get_or_404(standup_id)
    
    # Check if user already submitted an update
    existing_note = StandupNote.query.filter_by(
        meeting_id=standup_id,
        user_id=current_user.id
    ).first()
    
    if request.method == 'POST':
        yesterday = request.form['yesterday']
        today = request.form['today']
        blockers = request.form['blockers']
        
        if existing_note:
            # Update existing note
            existing_note.yesterday = yesterday
            existing_note.today = today
            existing_note.blockers = blockers
            existing_note.updated_at = datetime.utcnow()
        else:
            # Create new note
            note = StandupNote(
                meeting_id=standup_id,
                user_id=current_user.id,
                yesterday=yesterday,
                today=today,
                blockers=blockers
            )
            db.session.add(note)
        
        db.session.commit()
        flash_success('Your standup update has been submitted.')
        return redirect(url_for('meetings.view_standup', standup_id=standup_id))
    
    # GET request - show form
    return render_template(
        'meetings/standup/submit_update.html',
        standup=standup,
        existing_note=existing_note
    )


@bp.route('/standups/<int:standup_id>/action', methods=['POST'])
@login_required
def add_standup_action(standup_id):
    standup = StandupMeeting.query.get_or_404(standup_id)
    
    description = request.form['description']
    assignee_id = request.form.get('assignee_id')
    due_date_str = request.form.get('due_date')
    
    due_date = None
    if due_date_str:
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
    
    action_item = ActionItem(
        description=description,
        assignee_id=assignee_id,
        due_date=due_date,
        standup_meeting_id=standup_id
    )
    
    db.session.add(action_item)
    db.session.commit()
    
    flash_success('Action item added successfully.')
    return redirect(url_for('meetings.view_standup', standup_id=standup_id))


# Retrospective routes
@bp.route('/retrospectives/')
@login_required
def retrospectives():
    # Get all retrospectives, ordered by date (newest first)
    retrospectives = RetrospectiveMeeting.query.order_by(desc(RetrospectiveMeeting.date)).all()
    
    return render_template(
        'meetings/retrospective/index.html',
        retrospectives=retrospectives
    )


@bp.route('/retrospectives/new', methods=['GET', 'POST'])
@login_required
def new_retrospective():
    if request.method == 'POST':
        # Get form data
        sprint_id = request.form['sprint_id']
        retro_date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        start_time_str = request.form['start_time']
        start_time = datetime.strptime(start_time_str, '%H:%M').time()
        duration = int(request.form['duration'])
        meeting_link = request.form.get('meeting_link', '')
        
        # Check if a retrospective already exists for this sprint
        existing_retro = RetrospectiveMeeting.query.filter_by(sprint_id=sprint_id).first()
        if existing_retro:
            flash_error('A retrospective meeting already exists for this sprint.')
            return redirect(url_for('meetings.retrospectives'))
        
        # Create new retrospective
        retro = RetrospectiveMeeting(
            sprint_id=sprint_id,
            date=retro_date,
            start_time=start_time,
            duration_minutes=duration,
            meeting_link=meeting_link
        )
        
        db.session.add(retro)
        db.session.commit()
        
        flash_success('Retrospective meeting created successfully.')
        return redirect(url_for('meetings.retrospectives'))
    
    # GET request - show form
    completed_sprints = Sprint.query.filter_by(status='completed').all()
    return render_template('meetings/retrospective/new.html', sprints=completed_sprints)


@bp.route('/retrospectives/<int:retro_id>')
@login_required
def view_retrospective(retro_id):
    retro = RetrospectiveMeeting.query.get_or_404(retro_id)
    
    # Get items by category
    went_well_items = RetrospectiveItem.query.filter_by(
        meeting_id=retro_id, 
        category=RetrospectiveCategory.went_well
    ).order_by(desc(RetrospectiveItem.votes)).all()
    
    to_improve_items = RetrospectiveItem.query.filter_by(
        meeting_id=retro_id, 
        category=RetrospectiveCategory.to_improve
    ).order_by(desc(RetrospectiveItem.votes)).all()
    
    action_items = ActionItem.query.filter_by(retro_meeting_id=retro_id).all()
    
    # Get all users for action item assignment
    users = User.query.all()
    
    return render_template(
        'meetings/retrospective/view.html',
        retro=retro,
        went_well_items=went_well_items,
        to_improve_items=to_improve_items,
        action_items=action_items,
        users=users
    )


@bp.route('/retrospectives/<int:retro_id>/add_item', methods=['POST'])
@login_required
def add_retro_item(retro_id):
    retro = RetrospectiveMeeting.query.get_or_404(retro_id)
    
    category = request.form['category']
    content = request.form['content']
    
    item = RetrospectiveItem(
        meeting_id=retro_id,
        user_id=current_user.id,
        category=RetrospectiveCategory[category],
        content=content
    )
    
    db.session.add(item)
    db.session.commit()
    
    flash_success('Item added successfully.')
    return redirect(url_for('meetings.view_retrospective', retro_id=retro_id))


@bp.route('/retrospectives/<int:retro_id>/vote/<int:item_id>', methods=['POST'])
@login_required
def vote_retro_item(retro_id, item_id):
    item = RetrospectiveItem.query.get_or_404(item_id)
    
    # Increment vote count
    item.votes += 1
    db.session.commit()
    
    return {'success': True, 'votes': item.votes}


@bp.route('/retrospectives/<int:retro_id>/action', methods=['POST'])
@login_required
def add_retro_action(retro_id):
    retro = RetrospectiveMeeting.query.get_or_404(retro_id)
    
    description = request.form['description']
    assignee_id = request.form.get('assignee_id')
    due_date_str = request.form.get('due_date')
    
    due_date = None
    if due_date_str:
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
    
    action_item = ActionItem(
        description=description,
        assignee_id=assignee_id,
        due_date=due_date,
        retro_meeting_id=retro_id
    )
    
    db.session.add(action_item)
    db.session.commit()
    
    flash_success('Action item added successfully.')
    return redirect(url_for('meetings.view_retrospective', retro_id=retro_id))


# Action Items routes
@bp.route('/action-items/')
@login_required
def action_items():
    # Get all action items
    all_items = ActionItem.query.order_by(ActionItem.due_date).all()
    
    # Get my action items
    my_items = ActionItem.query.filter_by(assignee_id=current_user.id).order_by(ActionItem.due_date).all()
    
    # Get open action items
    open_items = ActionItem.query.filter_by(status='open').order_by(ActionItem.due_date).all()
    
    # Get users for filtering
    users = User.query.all()
    
    return render_template(
        'meetings/action_items/index.html',
        all_items=all_items,
        my_items=my_items,
        open_items=open_items,
        users=users
    )


@bp.route('/action-items/<int:item_id>/update', methods=['POST'])
@login_required
def update_action_item(item_id):
    item = ActionItem.query.get_or_404(item_id)
    
    status = request.form['status']
    item.status = status
    
    if status == 'completed':
        item.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    flash_success('Action item updated successfully.')
    return redirect(request.referrer or url_for('meetings.action_items'))


@bp.route('/action-items/new', methods=['GET', 'POST'])
@login_required
def new_action_item():
    if request.method == 'POST':
        description = request.form['description']
        assignee_id = request.form.get('assignee_id')
        due_date_str = request.form.get('due_date')
        
        due_date = None
        if due_date_str:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        
        action_item = ActionItem(
            description=description,
            assignee_id=assignee_id,
            due_date=due_date
        )
        
        db.session.add(action_item)
        db.session.commit()
        
        flash_success('Action item created successfully.')
        return redirect(url_for('meetings.action_items'))
    
    # GET request - show form
    users = User.query.all()
    return render_template('meetings/action_items/new.html', users=users)


# Calendar view
@bp.route('/calendar')
@login_required
def calendar():
    # Get all meetings for the next 30 days
    today = date.today()
    end_date = today + timedelta(days=30)
    
    standups = StandupMeeting.query.filter(
        StandupMeeting.date >= today,
        StandupMeeting.date <= end_date
    ).all()
    
    retrospectives = RetrospectiveMeeting.query.filter(
        RetrospectiveMeeting.date >= today,
        RetrospectiveMeeting.date <= end_date
    ).all()
    
    # Format meetings for calendar
    events = []
    
    for standup in standups:
        start_datetime = datetime.combine(standup.date, standup.start_time)
        end_datetime = start_datetime + timedelta(minutes=standup.duration_minutes)
        
        events.append({
            'id': f'standup-{standup.id}',
            'title': 'Daily Standup',
            'start': start_datetime.isoformat(),
            'end': end_datetime.isoformat(),
            'url': url_for('meetings.view_standup', standup_id=standup.id),
            'color': '#4CAF50'  # Green
        })
    
    for retro in retrospectives:
        start_datetime = datetime.combine(retro.date, retro.start_time)
        end_datetime = start_datetime + timedelta(minutes=retro.duration_minutes)
        
        events.append({
            'id': f'retro-{retro.id}',
            'title': f'Sprint Retrospective: {retro.sprint.name}',
            'start': start_datetime.isoformat(),
            'end': end_datetime.isoformat(),
            'url': url_for('meetings.view_retrospective', retro_id=retro.id),
            'color': '#9C27B0'  # Purple
        })
    
    return render_template('meetings/calendar.html', events=events)


# API endpoints for AJAX calls
@bp.route('/api/action-items/user/<int:user_id>')
@login_required
def api_user_action_items(user_id):
    items = ActionItem.query.filter_by(assignee_id=user_id).all()
    
    result = []
    for item in items:
        result.append({
            'id': item.id,
            'description': item.description,
            'status': item.status,
            'due_date': item.due_date.isoformat() if item.due_date else None
        })
    
    return result


@bp.route('/api/standup-notes/user/<int:user_id>')
@login_required
def api_user_standup_notes(user_id):
    # Get the last 5 standup notes for this user
    notes = StandupNote.query.filter_by(user_id=user_id).order_by(desc(StandupNote.created_at)).limit(5).all()
    
    result = []
    for note in notes:
        result.append({
            'id': note.id,
            'meeting_date': note.meeting.date.isoformat(),
            'yesterday': note.yesterday,
            'today': note.today,
            'blockers': note.blockers
        })
    
    return result
