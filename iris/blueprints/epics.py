from flask import Blueprint, render_template, request, redirect, url_for, flash
from iris.extensions import db
from iris.models import Epic, ProductIdea, StatusEnum
from iris.utils import flash_success

bp = Blueprint('epics', __name__, url_prefix='/epics')


@bp.route('/')
def index():
    epics = Epic.query.order_by(Epic.created_at.desc()).all()
    return render_template('epics/index.html', epics=epics)


@bp.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        priority = request.form.get('priority')
        goal = request.form.get('goal')
        tags = request.form.get('tags').split(',') if request.form.get('tags') else []
        status = StatusEnum[request.form.get('status', 'backlog')]
        product_idea_id = request.form.get('product_idea_id')
        
        epic = Epic(
            title=title,
            description=description,
            priority=priority,
            goal=goal,
            tags=tags,
            status=status,
            product_idea_id=product_idea_id if product_idea_id else None
        )
        
        db.session.add(epic)
        db.session.commit()
        
        flash_success('Epic created successfully!')
        return redirect(url_for('epics.index'))
    
    product_ideas = ProductIdea.query.all()
    return render_template('epics/new.html', product_ideas=product_ideas)


@bp.route('/<int:epic_id>')
def view(epic_id):
    epic = Epic.query.get_or_404(epic_id)
    return render_template('epics/view.html', epic=epic)
