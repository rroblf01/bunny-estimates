from typing import Annotated

from annotated_types import Len
from ninja import ModelSchema, Schema

from estimates.models import Task


class TaskSchema(ModelSchema):
    title: str
    description: str

    class Meta:
        model = Task
        fields = ["title", "description"]


class TaskListSchema(Schema):
    room_name: str
    tasks: Annotated[list[TaskSchema], Len(min_length=1)]


class TopicSchema(Schema):
    task__title: str
    task__description: str


class RoomOutSchema(Schema):
    name: str
    topics: list[TopicSchema]


class VoteResumeSchema(Schema):
    name: str
    value: float | None


class TopicResumeSchema(Schema):
    title: str
    description: str
    votes: list[VoteResumeSchema]
    average: float


class RoomResumeSchema(Schema):
    name: str
    finished: bool
    topics: list[TopicResumeSchema]
