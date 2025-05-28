from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class WebsiteCreate(BaseModel):
    name: str
    url: str

class BugReportCreate(BaseModel):
    title: str
    description: str
    website_id: int
    priority: str = "Medium"

class BugCommentCreate(BaseModel):
    comment: str
