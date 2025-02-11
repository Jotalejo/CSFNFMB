from fastapi.templating import Jinja2Templates
from .database import get_db

templates = Jinja2Templates(directory="templates")