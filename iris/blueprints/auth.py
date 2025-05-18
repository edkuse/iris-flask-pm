from flask import Blueprint, current_app, redirect, request, url_for, session, current_app, flash, render_template
from flask_login import login_user, logout_user, current_user, login_required
from iris.extensions import db
from iris.models import User
from iris.utils import flash_success, flash_error, flash_info
from datetime import datetime
import uuid
import msal
import os
import requests

bp = Blueprint('auth', __name__, url_prefix='/auth')


def _build_msal_app(cache=None, authority=None):
    """Build the MSAL application."""
    return msal.ConfidentialClientApplication(
        current_app.config.get('CLIENT_ID'),
        authority=authority or current_app.config.get('AUTHORITY'),
        client_credential=current_app.config.get('CLIENT_SECRET'),
        token_cache=cache
    )


def _build_auth_url(authority=None, scopes=None, state=None, prompt=None):
    """Build the authentication URL."""
    return _build_msal_app(authority=authority).get_authorization_request_url(
        scopes or current_app.config.get('SCOPE'),
        redirect_uri=current_app.config.get('REDIRECT_URI'),
        state=state or str(uuid.uuid4()),
        prompt=prompt
    )


def _get_token_from_cache(scope=None):
    """Get token from cache."""
    cache = _load_cache()
    cca = _build_msal_app(cache=cache)
    accounts = cca.get_accounts()
    if accounts:
        result = cca.acquire_token_silent(
            scope or current_app.config.get('SCOPE'),
            account=accounts[0]
        )
        _save_cache(cache)
        return result
    return None


def _load_cache():
    """Load the token cache."""
    cache = msal.SerializableTokenCache()
    if session.get("token_cache"):
        cache.deserialize(session["token_cache"])
    return cache


def _save_cache(cache):
    """Save the token cache."""
    if cache.has_state_changed:
        session["token_cache"] = cache.serialize()


@bp.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    # Generate and store a state for CSRF protection
    session["state"] = str(uuid.uuid4())
    
    # Build the auth URL and redirect to Microsoft login
    auth_url = _build_auth_url(scopes=current_app.config.get('SCOPE'), state=session["state"])
    return redirect(auth_url)


@bp.route('/switch-account')
def switch_account():
    """Initiate the account switching process."""
    # Generate and store a state for CSRF protection
    session["state"] = str(uuid.uuid4())
    
    # Build the auth URL with prompt=select_account to force account selection
    auth_url = _build_auth_url(
        scopes=current_app.config.get('SCOPE'), 
        state=session["state"],
        prompt="select_account"
    )
    
    current_app.logger.info(f"Switching account, redirecting to: {auth_url}")
    
    # Store the fact that we're switching accounts
    session["switching_account"] = True
    
    return redirect(auth_url)


@bp.route('/logout')
def logout():
    """Log out the current user."""
    # Get user info for flash message
    user_name = current_user.display_name if current_user.is_authenticated else "User"
    
    # Log out the user
    logout_user()
    
    # Clear the session
    session.clear()
    
    # Flash a message
    flash_success(f"You have been logged out successfully. Goodbye, {user_name}!")
    
    # Redirect to the login page
    return redirect(url_for('dashboard.index'))


@bp.route('/logout-confirm')
def logout_confirm():
    """Show logout confirmation page."""
    return render_template('auth/logout_confirm.html')


@bp.route('/callback')
def callback():
    current_app.logger.info("Callback received")
    
    # Check if there's an error in the request
    if "error" in request.args:
        error = request.args.get("error")
        error_description = request.args.get("error_description", "Unknown error")
        current_app.logger.error(f"Auth error: {error} - {error_description}")

        flash_error(f"Authentication error: {error_description}")
        return redirect(url_for('dashboard.index'))
    
    # Verify state for CSRF protection
    if request.args.get('state') != session.get("state"):
        current_app.logger.error("State verification failed")
        flash_error("State verification failed. The request might have been tampered with.")

        return redirect(url_for('dashboard.index'))
    
    # Get token from the callback
    cache = _load_cache()
    cca = _build_msal_app(cache=cache)
    
    try:
        current_app.logger.info("Acquiring token by authorization code")
        result = cca.acquire_token_by_authorization_code(
            request.args.get('code'),
            scopes=current_app.config.get('SCOPE'),
            redirect_uri=current_app.config.get('REDIRECT_URI')
        )
        
        _save_cache(cache)
        
        if "error" in result:
            current_app.logger.error(f"Token acquisition failed: {result.get('error_description', 'Unknown error')}")
            flash_error(f"Token acquisition failed: {result.get('error_description', 'Unknown error')}")
            return redirect(url_for('dashboard.index'))
        
        # Get user info from Microsoft Graph
        current_app.logger.info("Getting user info from Microsoft Graph")
        access_token = result["access_token"]
        graph_data = requests.get(
            "https://graph.microsoft.com/v1.0/me",
            headers={'Authorization': f'Bearer {access_token}'},
        ).json()
        
        current_app.logger.info(f"Graph data received: {graph_data}")
        
        # Check if user exists, if not create a new one
        user_id = graph_data.get("id")

        if not user_id:
            current_app.logger.error("No user ID received from Microsoft Graph")
            flash_error("Failed to get user information from Microsoft. Please try again.")

            return redirect(url_for('dashboard.index'))
        
        user = User.query.filter_by(id=user_id).first()
        
        # Try to get user's profile photo
        profile_picture_url = None

        try:
            # First check if the user has a profile photo
            photo_response = requests.get(
                "https://graph.microsoft.com/v1.0/me/photo/$value",
                headers={'Authorization': f'Bearer {access_token}'},
                stream=True
            )

            current_app.logger.info(photo_response.status_code)
            
            if photo_response.status_code == 200:
                # Save the photo to a static folder
                photo_path = f"static/profile_pictures/{user_id}.jpg"
                os.makedirs(os.path.dirname(photo_path), exist_ok=True)
                
                with open(photo_path, 'wb') as f:
                    for chunk in photo_response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                
                profile_picture_url = f"/{photo_path}"
                current_app.logger.info(f"Profile picture saved to {photo_path}")

        except Exception as e:
            current_app.logger.warning(f"Failed to get profile picture: {str(e)}")
        
        if not user:
            current_app.logger.info(f"Creating new user with ID: {user_id}")

            user = User(
                id=user_id,
                email=graph_data.get("mail") or graph_data.get("userPrincipalName"),
                display_name=graph_data.get("displayName", "Unknown User"),
                job_title=graph_data.get("jobTitle"),
                department=graph_data.get("department"),
                profile_picture=profile_picture_url
            )
            db.session.add(user)

        else:
            current_app.logger.info(f"User found: {user.display_name}")

            # Update user information
            user.email = graph_data.get("mail") or graph_data.get("userPrincipalName") or user.email
            user.display_name = graph_data.get("displayName") or user.display_name
            user.job_title = graph_data.get("jobTitle") or user.job_title
            user.department = graph_data.get("department") or user.department

            if profile_picture_url:
                user.profile_picture = profile_picture_url
        
        # Update last login time
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Log the user in
        login_user(user)
        
        current_app.logger.info(f"User {user.display_name} logged in successfully")
        flash_success(f"Welcome, {user.display_name}!")
        
        # Redirect to the main page or the page the user was trying to access
        return redirect(request.args.get('next') or url_for('dashboard.index'))
    
    except Exception as e:
        current_app.logger.exception("Error during callback processing")
        flash_error(f"An error occurred during authentication: {str(e)}")

        return redirect(url_for('dashboard.index'))


@bp.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html', user=current_user)


@bp.route('/test-login')
def test_login():
    """Test login endpoint for debugging"""
    # Create a test user if it doesn't exist
    test_user = User.query.filter_by(id="test-user-id").first()
    if not test_user:
        test_user = User(
            id="test-user-id",
            email="test@example.com",
            display_name="Test User",
            job_title="Developer",
            department="Engineering",
            profile_picture=None  # No profile picture for test user
        )
        db.session.add(test_user)
        db.session.commit()
    
    # Log in the test user
    login_user(test_user)
    session["user"] = {
        "id": test_user.id,
        "name": test_user.display_name,
        "email": test_user.email,
        "job_title": test_user.job_title,
        "department": test_user.department,
        "profile_picture": test_user.profile_picture
    }
    
    flash_success(f"Logged in as test user: {test_user.display_name}")
    return redirect(url_for('dashboard.index'))


@bp.route('/dev-login', methods=['GET', 'POST'])
def dev_login():
    """Development login endpoint"""
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        
        if not email or not name:
            flash_error("Email and name are required")
            return render_template('auth/dev_login.html')
        
        # Find or create user
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(
                id=str(uuid.uuid4()),
                email=email,
                display_name=name,
                job_title="Developer",
                department="Engineering",
                profile_picture=None  # No profile picture for dev login
            )
            db.session.add(user)
            db.session.commit()
        
        # Log in the user
        login_user(user)
        session["user"] = {
            "id": user.id,
            "name": user.display_name,
            "email": user.email,
            "job_title": user.job_title,
            "department": user.department,
            "profile_picture": user.profile_picture
        }
        
        flash_success(f"Logged in as: {user.display_name}")
        return redirect(url_for('dashboard.index'))
    
    return render_template('auth/dev_login.html')
