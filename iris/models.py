from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import ARRAY
from .extensions import db
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


class User(db.Model, UserMixin):
    __tablename__ = "users"
    
    id = db.Column(db.String(36), primary_key=True)  # Using MS object ID as primary key
    email = db.Column(db.String(255), unique=True, nullable=False)
    display_name = db.Column(db.String(255), nullable=False)
    job_title = db.Column(db.String(255), nullable=True)
    department = db.Column(db.String(255), nullable=True)
    profile_picture = db.Column(db.String(1024), nullable=True)  # Add this line
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    
    # Add relationships for tasks assigned to this user
    assigned_tasks = db.relationship('Task', backref='assigned_user', lazy=True, 
                                  foreign_keys='Task.assignee_id')
    
    # Add relationship for comments authored by this user
    comments = db.relationship('Comment', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.email}>"


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
    # Add creator relationship
    creator_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    creator = db.relationship('User', backref='product_ideas')
    
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
    creator = db.relationship('User', backref='epics')
    # user_stories = db.relationship('UserStory', backref='epic', lazy=True)


class Sprint(db.Model):
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
    epic_id = db.Column(db.Integer, db.ForeignKey('epic.id'), nullable=True)
    sprint_id = db.Column(db.Integer, db.ForeignKey('sprint.id'), nullable=True)
    story_points = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Relationships
    # tasks = db.relationship('Task', backref='user_story', lazy=True)
    # comments = db.relationship('Comment', backref='user_story', lazy=True)
    
    def __repr__(self):
        return f'<UserStory {self.title}>'


class Task(db.Model):
    __tablename__ = "tasks"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.Enum(StatusEnum), default=StatusEnum.todo)
    # Update assignee to be a proper foreign key
    assignee_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    # Keep original assignee field for backward compatibility
    assignee = db.Column(db.String(100))
    effort = db.Column(db.String(50))
    due_date = db.Column(db.DateTime)
    story_id = db.Column(db.Integer, db.ForeignKey('user_stories.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relationships
    creator_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    creator = db.relationship('User', backref='created_tasks', foreign_keys=[creator_id])
    comments = db.relationship('Comment', backref='task', lazy=True)

    def __repr__(self):
        return f'<Task {self.title}>'


class Comment(db.Model):
    __tablename__ = "comments"
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    # Update author to be a proper foreign key
    author_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    # Keep original author field for backward compatibility
    author = db.Column(db.String(100))
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    story_id = db.Column(db.Integer, db.ForeignKey('user_stories.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Comment {self.id}>'
