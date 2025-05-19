from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from iris.extensions import db
from iris.models import Role, Permission, User
from iris.utils.flash import flash_success, flash_error
from iris.utils.rbac import admin_required

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/')
@login_required
@admin_required
def index():
    return render_template('admin/index.html')


@bp.route('/roles')
@login_required
@admin_required
def roles():
    roles = Role.query.all()
    return render_template('admin/roles/index.html', roles=roles)


@bp.route('/roles/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_role():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        # Check if role already exists
        existing_role = Role.query.filter_by(name=name).first()
        if existing_role:
            flash_error(f'Role "{name}" already exists')
            return redirect(url_for('admin.new_role'))
        
        # Create new role
        role = Role(name=name, description=description)
        
        # Add permissions
        permission_ids = request.form.getlist('permissions')
        if permission_ids:
            permissions = Permission.query.filter(Permission.id.in_(permission_ids)).all()
            role.permissions = permissions
        
        db.session.add(role)
        db.session.commit()
        
        flash_success(f'Role "{name}" created successfully')
        return redirect(url_for('admin.roles'))
    
    permissions = Permission.query.all()
    return render_template('admin/roles/new.html', permissions=permissions)


@bp.route('/roles/<int:role_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_role(role_id):
    role = Role.query.get_or_404(role_id)
    
    # Prevent editing system roles
    if role.is_system_role:
        flash_error('System roles cannot be edited')
        return redirect(url_for('admin.roles'))
    
    if request.method == 'POST':
        role.name = request.form.get('name')
        role.description = request.form.get('description')
        
        # Update permissions
        permission_ids = request.form.getlist('permissions')
        permissions = Permission.query.filter(Permission.id.in_(permission_ids)).all()
        role.permissions = permissions
        
        db.session.commit()
        
        flash_success(f'Role "{role.name}" updated successfully')
        return redirect(url_for('admin.roles'))
    
    permissions = Permission.query.all()
    return render_template('admin/roles/edit.html', role=role, permissions=permissions)


@bp.route('/roles/<int:role_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_role(role_id):
    role = Role.query.get_or_404(role_id)
    
    # Prevent deleting system roles
    if role.is_system_role:
        flash_error('System roles cannot be deleted')
        return redirect(url_for('admin.roles'))
    
    db.session.delete(role)
    db.session.commit()
    
    flash_success(f'Role "{role.name}" deleted successfully')
    return redirect(url_for('admin.roles'))


@bp.route('/users')
@login_required
@admin_required
def users():
    users = User.query.all()
    return render_template('admin/users/index.html', users=users)


@bp.route('/users/<user_id>/roles', methods=['GET', 'POST'])
@login_required
@admin_required
def user_roles(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        # Update user roles
        role_ids = request.form.getlist('roles')
        roles = Role.query.filter(Role.id.in_(role_ids)).all()
        user.roles = roles
        
        db.session.commit()
        
        flash_success(f'Roles for {user.display_name} updated successfully')
        return redirect(url_for('admin.users'))
    
    roles = Role.query.all()
    return render_template('admin/users/roles.html', user=user, roles=roles)
