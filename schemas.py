from pydantic import BaseModel, constr, validator
from typing import Optional
from datetime import datetime
from models import TaskStatus, TaskPriority


class TaskCreate(BaseModel):
    title: constr(strip_whitespace=True, min_length=1, max_length=200) # type: ignore
    description: Optional[constr(max_length=1000)] = None # type: ignore
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    assigned_to: Optional[constr(max_length=100)] = None # type: ignore

    @validator("title")
    def check_title(cls, val):
        if not val or not val.strip():
            raise ValueError("Title can't be empty")
        return val.strip()

    @validator("due_date")
    def check_due_date(cls, val):
        if val is not None:
            from datetime import datetime
            if val <= datetime.utcnow():
                raise ValueError("Due date must be in the future")
        return val


class TaskUpdate(BaseModel):
    title: Optional[constr(strip_whitespace=True,
                           min_length=1, max_length=200)] = None # type: ignore
    description: Optional[constr(max_length=1000)] = None # type: ignore
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    assigned_to: Optional[constr(max_length=100)] = None # type: ignore

    @validator("title")
    def check_title(cls, val):
        if val is not None and not val.strip():
            raise ValueError("Title can't be empty")
        return val.strip() if val else val

    @validator("due_date")
    def check_due_date(cls, val):
        if val is not None:
            from datetime import datetime
            if val <= datetime.utcnow():
                raise ValueError("Due date must be in the future")
        return val


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    created_at: datetime
    updated_at: Optional[datetime]
    due_date: Optional[datetime]
    assigned_to: Optional[str]

    class Config:
        orm_mode = True
