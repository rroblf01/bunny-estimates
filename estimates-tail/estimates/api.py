from uuid import UUID

from asgiref.sync import sync_to_async
from ninja import Router

from estimates.models import Room, Task, Topic
from estimates.schemas import RoomOutSchema, RoomResumeSchema, TaskListSchema

router = Router()


@router.post("/room")
async def create_room(request, payload: TaskListSchema):
    room = await Room.objects.acreate(name=payload.room_name)
    for task_data in payload.tasks:
        task = await Task.objects.acreate(
            title=task_data.title, description=task_data.description
        )
        await Topic.objects.acreate(task=task, room=room)
    return {"public_name": room.public_name}


@router.get("/room/{public_name}", response=RoomOutSchema)
async def get_room(request, public_name: UUID):
    room = await Room.objects.aget(public_name=public_name)
    topics = await sync_to_async(list)(
        Topic.objects.filter(room=room).values("task__title", "task__description")
    )

    return {
        "name": room.name,
        "topics": topics,
    }


@router.get("/room/{public_name}/resume", response={200: RoomResumeSchema, 404: str})
async def get_room_resume(request, public_name: UUID):
    try:
        room = await Room.objects.aget(public_name=public_name)
    except Room.DoesNotExist:
        return 404, "Room not found"

    topics = []
    async for topic in room.topic_set.select_related("task").all().order_by("id"):
        topic_data = {
            "title": topic.task.title,
            "description": topic.task.description,
            "votes": [],
            "average": await topic.average_votes,
        }
        async for vote in topic.vote_set.all().order_by("id"):
            if vote.point_value:
                topic_data["votes"].append(
                    {
                        "value": vote.point_value,
                        "name": vote.voter_name,
                    }
                )
        topics.append(topic_data)

    return 200, {
        "name": room.name,
        "finished": await room.finished,
        "topics": topics,
    }
