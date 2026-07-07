from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TaskCreate(BaseModel):
    """Request body for creating a task."""

    title: str = Field(
        min_length=1,
        max_length=30,
        description="Short title for the task (1-30 characters).",
        examples=["Buy groceries"],
    )


class TaskResponse(BaseModel):
    """A single task as returned by the API."""

    model_config = ConfigDict(from_attributes=True)
    id: str = Field(description="Unique identifier of the task.")
    title: str = Field(description="Title of the task.")
    done: bool = Field(description="Whether the task has been completed.")
    created_at: datetime = Field(description="When the task was created (ISO 8601).")


class TaskListResponse(BaseModel):
    """Response body for listing tasks."""

    tasks: list[TaskResponse] = Field(description="All stored tasks.")


class TaskUpdate(BaseModel):
    """Request body for renaming a task."""

    title: str = Field(
        min_length=1,
        max_length=30,
        description="New title for the task (1-30 characters).",
        examples=["Buy groceries and fruit"],
    )
