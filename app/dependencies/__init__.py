from fastapi.templating import Jinja2Templates
from .database import get_db
from .auth import get_current_user


templates = Jinja2Templates(directory="templates")