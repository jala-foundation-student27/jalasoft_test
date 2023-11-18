from pydantic import BaseModel,ConfigDict
from datetime import datetime
from enum import Enum

class Status(Enum):
    status = "completed"
    overdue = "overdue"

class Todo_list_model(BaseModel):  # Model Restricting the types of the fields
    model_config = ConfigDict(extra="forbid") # forbid extra fields in the model
    task:str
    deadline:datetime
    category:str
    status: Enum
    description:str | None
    lastUpdated:datetime

    def to_dict(self) ->dict:
        return dict(self)

# data = {"deadline": "2023-08-22 15:30:00"}
# todo_data = {"task":"task",
#              "deadline":"2023-08-22 15:30:00","category":"Good","status":Status.completed,"description":"lorem"}
# list = Todo_list_model(**todo_data)
# print(dict(Status.completed))