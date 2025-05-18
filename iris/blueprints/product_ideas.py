from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from iris.extensions import db
from iris.models import ProductIdea
from iris.utils import flash_success

product_ideas_bp = Blueprint('product_ideas', __name__)


@product_ideas_bp.route('/')
@login_required
def index():
    ideas = ProductIdea.query.order_by(ProductIdea.created_at.desc()).all()
    return render_template('product_ideas/index.html', ideas=ideas)


@product_ideas_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        tags = request.form.get('tags').split(',') if request.form.get('tags') else []
        problem_statement = request.form.get('problem_statement')
        success_metrics = request.form.get('success_metrics')
        impact_level = request.form.get('impact_level')
        
        idea = ProductIdea(
            title=title,
            description=description,
            tags=tags,
            problem_statement=problem_statement,
            success_metrics=success_metrics,
            impact_level=impact_level,
            creator_id=current_user.id  # Set the creator to the current user
        )
        
        db.session.add(idea)
        db.session.commit()
        
        flash_success('Product idea created successfully!')
        return redirect(url_for('product_ideas.index'))
    
    return render_template('product_ideas/new.html')


@product_ideas_bp.route('/<int:idea_id>')
@login_required
def view(idea_id):
    idea = ProductIdea.query.get_or_404(idea_id)
    return render_template('product_ideas/view.html', idea=idea)
