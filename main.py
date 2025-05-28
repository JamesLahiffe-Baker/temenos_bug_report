from fastapi import FastAPI
from database import Base, engine
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from controllers import (
    auth_controller,
    dashboard_controller,
    bug_controller,
    website_controller,
    user_controller
)

#Init
Base.metadata.create_all(bind=engine)
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

#Included routers
app.include_router(auth_controller.router)
app.include_router(dashboard_controller.router)
app.include_router(bug_controller.router)
app.include_router(website_controller.router)
app.include_router(user_controller.router)
