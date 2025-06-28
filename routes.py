from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime

import db
from models import Task, TaskStatus, TaskPriority
from schemas import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter()


@router.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate):
    session = db.get_session()
    new_task = Task(
        title=task.title.strip(),
        description=task.description,
        status=task.status or TaskStatus.pending,
        priority=task.priority or TaskPriority.medium,
        due_date=task.due_date,
        assigned_to=task.assigned_to
    )
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    session.close()
    return new_task


@router.get("/tasks", response_model=List[TaskResponse])
def list_tasks(
    skip: int = 0,
    limit: int = 10,
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None
):
    session = db.get_session()
    query = select(Task)
    if status:
        query = query.where(Task.status == status)
    if priority:
        query = query.where(Task.priority == priority)
    tasks = session.exec(query.offset(skip).limit(limit)).all()
    session.close()
    return tasks


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    session = db.get_session()
    task = session.get(Task, task_id)
    session.close()
    if not task:
        raise HTTPException(404, detail="Task not found")
    return task


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, changes: TaskUpdate):
    session = db.get_session()
    task = session.get(Task, task_id)
    if not task:
        session.close()
        raise HTTPException(404, detail="Task not found")
    updated = changes.dict(exclude_unset=True)
    for key, value in updated.items():
        setattr(task, key, value)
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    session.close()
    return task


@router.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    session = db.get_session()
    task = session.get(Task, task_id)
    if not task:
        session.close()
        raise HTTPException(404, detail="Task not found")
    session.delete(task)
    session.commit()
    session.close()
    return


@router.get("/tasks/status/{status}", response_model=List[TaskResponse])
def tasks_by_status(status: TaskStatus, skip: int = 0, limit: int = 10):
    session = db.get_session()
    tasks = session.exec(
        select(Task).where(Task.status == status).offset(skip).limit(limit)
    ).all()
    session.close()
    return tasks


@router.get("/tasks/priority/{priority}", response_model=List[TaskResponse])
def tasks_by_priority(priority: TaskPriority, skip: int = 0, limit: int = 10):
    session = db.get_session()
    tasks = session.exec(
        select(Task).where(Task.priority == priority).offset(skip).limit(limit)
    ).all()
    session.close()
    return tasks
