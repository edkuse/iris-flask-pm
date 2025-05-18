import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Microsoft Entra ID configuration
    CLIENT_ID = os.getenv('MS_CLIENT_ID')
    CLIENT_SECRET = os.getenv('MS_CLIENT_SECRET')
    TENANT_ID = os.getenv('MS_TENANT_ID')
    AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
    REDIRECT_PATH = "/auth/callback"  # Used for the redirect URI
    SCOPE = ["User.Read"]  # Default scope for authentication
    SESSION_TYPE = "filesystem"  # Session storage type
    SESSION_FILE_DIR = "./iris/sessions"
    
    # App configuration
    APP_URL = os.environ.get('APP_URL')
    REDIRECT_URI = f"{APP_URL}{REDIRECT_PATH}"
