from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class TaskCreate(BaseModel):
    title: str = Field(min_length =1, max_length = 30)
    
    
class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    id: str
    title: str
    done: bool
    #created_at: datetime
    
class TaskListResponse(BaseModel):
    tasks: list[TaskResponse]
