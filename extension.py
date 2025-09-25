from flask_sqlalchemy import SQLAlchemy #pyright: ignore[reportMissingImports] 
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
