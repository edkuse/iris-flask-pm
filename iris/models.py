from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import ARRAY
from iris.extensions import db
from datetime import datetime
import enum


class StatusEnum(enum.Enum):
    backlog = "backlog"
    in_progress = "in_progress"
    review = "review"
    done = "done"
    todo = "todo"


class SprintStatusEnum(str, enum.Enum):
    planning = "Planning"
    active = "Active"
    completed = "Completed"


class MeetingType(enum.Enum):
    standup = "standup"
    planning = "planning"
    review = "review"
    retrospective = "retrospective"
    other = "other"


class MeetingStatusEnum(str, enum.Enum):
    scheduled = "Scheduled"
    in_progress = "In Progress"
    completed = "Completed"


class RetrospectiveCategory(enum.Enum):
    went_well = "went_well"
    to_improve = "to_improve"
    action_item = "action_item"


# Association table for many-to-many relationship between users and roles
user_roles = db.Table('user_roles',
    db.Column('user_id', db.String(36), db.ForeignKey('users.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)
)

# Association table for many-to-many relationship between roles and permissions
role_permissions = db.Table('role_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'), primary_key=True)
)


class User(db.Model, UserMixin):
    __tablename__ = "users"
    
    id = db.Column(db.String(36), primary_key=True)  # Using MS object ID as primary key
    email = db.Column(db.String(255), unique=True, nullable=False)
    display_name = db.Column(db.String(255), nullable=False)
    job_title = db.Column(db.String(255), nullable=True)
    department = db.Column(db.String(255), nullable=True)
    profile_picture = db.Column(db.String(1024), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    
    # Add roles relationship
    roles = db.relationship('Role', secondary=user_roles, backref=db.backref('users', lazy='dynamic'))
    
    # Existing relationships
    assigned_tasks = db.relationship('Task', backref='assigned_user', lazy=True, foreign_keys='Task.assignee_id')
    comments = db.relationship('Comment', backref='user', lazy=True)
    product_ideas = db.relationship('ProductIdea', backref='creator', lazy=True)
    epics = db.relationship('Epic', backref='creator', lazy=True)
    created_tasks = db.relationship('Task', backref='creator', lazy=True, foreign_keys='Task.creator_id')
    standup_notes = db.relationship('StandupNote', backref='user', lazy=True)
    action_items = db.relationship('ActionItem', backref='assignee', lazy=True, foreign_keys='ActionItem.assignee_id')
    created_action_items = db.relationship('ActionItem', backref='creator', lazy=True, foreign_keys='ActionItem.creator_id')
    retrospective_items = db.relationship('RetrospectiveItem', backref='user', lazy=True)
    
    def __repr__(self):
        return f"<User {self.email}>"
    
    # Role-based methods
    def has_role(self, role_name):
        """Check if user has a specific role by name"""
        return any(role.name == role_name for role in self.roles)
    
    def has_permission(self, resource, action):
        """Check if user has permission to perform action on resource"""
        for role in self.roles:
            for permission in role.permissions:
                if permission.resource == resource and permission.action == action:
                    return True
        return False
    
    def is_admin(self):
        """Shortcut to check if user is an admin"""
        return self.has_role('admin')


class ProductIdea(db.Model):
    __tablename__ = "product_ideas"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    tags = db.Column(ARRAY(db.String))
    problem_statement = db.Column(db.Text)
    success_metrics = db.Column(db.Text)
    impact_level = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    creator_id = db.Column(db.String(36), db.ForeignKey('users.id'))

    # Relationships
    epics = db.relationship('Epic', backref='product_idea', lazy=True)


class Epic(db.Model):
    __tablename__ = "epics"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.String(50))
    goal = db.Column(db.Text)
    tags = db.Column(ARRAY(db.String))
    status = db.Column(db.Enum(StatusEnum), default=StatusEnum.backlog)
    product_idea_id = db.Column(db.Integer, db.ForeignKey('product_ideas.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    creator_id = db.Column(db.String(36), db.ForeignKey('users.id'))

    # Relationships
    user_stories = db.relationship('UserStory', backref='epic', lazy=True)


class Sprint(db.Model):
    __tablename__ = "sprints"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    goal = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum(SprintStatusEnum), default=SprintStatusEnum.planning)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Relationships
    user_stories = db.relationship('UserStory', backref='sprint', lazy=True)
    
    # New relationships for meetings
    standup_meetings = db.relationship('StandupMeeting', backref='sprint', lazy=True)
    retrospective = db.relationship('RetrospectiveMeeting', backref='sprint', uselist=False, lazy=True)
    
    def __repr__(self):
        return f'<Sprint {self.name}>'
    
    @property
    def total_story_points(self):
        return sum(story.story_points or 0 for story in self.user_stories)
    
    @property
    def completed_story_points(self):
        return sum((story.story_points or 0) for story in self.user_stories if story.status == StatusEnum.done)
    
    @property
    def progress_percentage(self):
        if self.total_story_points == 0:
            return 0
        return int((self.completed_story_points / self.total_story_points) * 100)
    
    @property
    def days_remaining(self):
        if self.end_date < datetime.utcnow():
            return 0
        return (self.end_date - datetime.utcnow()).days
    
    @property
    def days_total(self):
        return (self.end_date - self.start_date).days
    
    @property
    def is_active(self):
        now = datetime.utcnow()
        return self.start_date <= now <= self.end_date and self.status == SprintStatusEnum.active


class UserStory(db.Model):
    __tablename__ = "user_stories"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    goal = db.Column(db.Text, nullable=False)
    benefit = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), nullable=True)
    status = db.Column(db.Enum(StatusEnum), default=StatusEnum.backlog)
    epic_id = db.Column(db.Integer, db.ForeignKey('epics.id'), nullable=True)
    sprint_id = db.Column(db.Integer, db.ForeignKey('sprints.id'), nullable=True)
    story_points = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Relationships
    tasks = db.relationship('Task', backref='user_story', lazy=True)
    comments = db.relationship('Comment', backref='user_story', lazy=True)
    
    def __repr__(self):
        return f'<UserStory {self.title}>'


class Task(db.Model):
    __tablename__ = "tasks"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.Enum(StatusEnum), default=StatusEnum.todo)
    assignee_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    # Keep original assignee field for backward compatibility
    assignee = db.Column(db.String(100))
    effort = db.Column(db.String(50))
    due_date = db.Column(db.DateTime)
    story_id = db.Column(db.Integer, db.ForeignKey('user_stories.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    creator_id = db.Column(db.String(36), db.ForeignKey('users.id'))

    # Relationships
    comments = db.relationship('Comment', backref='task', lazy=True)

    def __repr__(self):
        return f'<Task {self.title}>'


class Comment(db.Model):
    __tablename__ = "comments"
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    # Keep original author field for backward compatibility
    author = db.Column(db.String(100))
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=True)
    story_id = db.Column(db.Integer, db.ForeignKey('user_stories.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Comment {self.id}>'


# New models for meeting management

class StandupMeeting(db.Model):
    __tablename__ = "standup_meetings"
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    sprint_id = db.Column(db.Integer, db.ForeignKey('sprints.id'), nullable=True)
    status = db.Column(db.Enum(MeetingStatusEnum), default=MeetingStatusEnum.scheduled)
    start_time = db.Column(db.Time, nullable=False)
    duration_minutes = db.Column(db.Integer, default=15)
    meeting_link = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    creator_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    
    # Relationships
    notes = db.relationship('StandupNote', backref='meeting', lazy=True, cascade="all, delete-orphan")
    action_items = db.relationship('ActionItem', backref='standup_meeting', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<StandupMeeting {self.date}>'


class StandupNote(db.Model):
    __tablename__ = "standup_notes"
    
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('standup_meetings.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    yesterday = db.Column(db.Text)  # What did I do yesterday?
    today = db.Column(db.Text)      # What will I do today?
    blockers = db.Column(db.Text)   # Any blockers?
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<StandupNote {self.id} by {self.user_id}>'


class RetrospectiveMeeting(db.Model):
    __tablename__ = "retrospective_meetings"
    
    id = db.Column(db.Integer, primary_key=True)
    sprint_id = db.Column(db.Integer, db.ForeignKey('sprints.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum(MeetingStatusEnum), default=MeetingStatusEnum.scheduled)
    start_time = db.Column(db.Time, nullable=False)
    duration_minutes = db.Column(db.Integer, default=60)
    meeting_link = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    creator_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    
    # Relationships
    items = db.relationship('RetrospectiveItem', backref='meeting', lazy=True, cascade="all, delete-orphan")
    action_items = db.relationship('ActionItem', backref='retro_meeting', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<RetrospectiveMeeting for Sprint {self.sprint_id}>'


class RetrospectiveItem(db.Model):
    __tablename__ = "retrospective_items"
    
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('retrospective_meetings.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    category = db.Column(db.Enum(RetrospectiveCategory), nullable=False)
    content = db.Column(db.Text, nullable=False)
    votes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<RetrospectiveItem {self.id} - {self.category.name}>'


class ActionItem(db.Model):
    __tablename__ = "action_items"
    
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    assignee_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    due_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(20), default='open')  # open, in-progress, completed
    standup_meeting_id = db.Column(db.Integer, db.ForeignKey('standup_meetings.id'), nullable=True)
    retro_meeting_id = db.Column(db.Integer, db.ForeignKey('retrospective_meetings.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    creator_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    
    def __repr__(self):
        return f'<ActionItem {self.id}>'


class Role(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))
    is_system_role = db.Column(db.Boolean, default=False)  # Flag for system-defined roles
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Relationships
    permissions = db.relationship('Permission', secondary=role_permissions, backref=db.backref('roles', lazy='dynamic'))
    
    def __repr__(self):
        return f'<Role {self.name}>'


class Permission(db.Model):
    __tablename__ = 'permissions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255))
    resource = db.Column(db.String(50), nullable=False)  # e.g., 'product_idea', 'epic', etc.
    action = db.Column(db.String(50), nullable=False)    # e.g., 'create', 'read', 'update', 'delete'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Permission {self.name}>'
