from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from iris.extensions import db
from iris.models import ProductIdea
from iris.utils import flash_success

bp = Blueprint('product_ideas', __name__, url_prefix='/product-ideas')


@bp.route('/')
@login_required
def index():
    ideas = ProductIdea.query.order_by(ProductIdea.created_at.desc()).all()
    return render_template('product_ideas/index.html', ideas=ideas)


@bp.route('/new', methods=['GET', 'POST'])
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


@bp.route('/<int:idea_id>')
@login_required
def view(idea_id):
    idea = ProductIdea.query.get_or_404(idea_id)
    return render_template('product_ideas/view.html', idea=idea)


@bp.route('/<int:idea_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(idea_id):
    idea = ProductIdea.query.get_or_404(idea_id)
    
    # Check if the current user is the creator or has permission to edit
    # This is a simple check - you might want to implement more complex permission logic
    # if current_user.id != idea.creator_id and not current_user.is_admin:
    #     flash('You do not have permission to edit this product idea.', 'error')
    #     return redirect(url_for('product_ideas.view', idea_id=idea.id))
    
    if request.method == 'POST':
        # Update the product idea with the form data
        idea.title = request.form.get('title')
        idea.description = request.form.get('description')
        idea.tags = request.form.get('tags').split(',') if request.form.get('tags') else []
        idea.problem_statement = request.form.get('problem_statement')
        idea.success_metrics = request.form.get('success_metrics')
        idea.impact_level = request.form.get('impact_level')
        
        # Save the changes
        db.session.commit()
        
        flash_success('Product idea updated successfully!')
        return redirect(url_for('product_ideas.view', idea_id=idea.id))
    
    # For GET requests, render the edit form with the current data
    return render_template('product_ideas/edit.html', product_idea=idea)


@bp.route('/<int:idea_id>/delete', methods=['POST'])
@login_required
def delete(idea_id):
    idea = ProductIdea.query.get_or_404(idea_id)
    
    # Check if the current user is the creator or has permission to delete
    # if current_user.id != idea.creator_id and not current_user.is_admin:
    #     flash('You do not have permission to delete this product idea.', 'error')
    #     return redirect(url_for('product_ideas.view', idea_id=idea.id))
    
    db.session.delete(idea)
    db.session.commit()
    
    flash_success('Product idea deleted successfully!')
    return redirect(url_for('product_ideas.index'))
