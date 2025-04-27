from enum import Enum
import datetime

class TaskStatus(Enum):
    Todo = "Todo"
    InProgress = "In Progress"
    Completed = "Completed"

class Task:
    title: str
    description: str
    status: TaskStatus
    createdAt: datetime.date
    updatedAt: datetime.date