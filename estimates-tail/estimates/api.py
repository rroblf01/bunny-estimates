from asgiref.sync import sync_to_async
from ninja import Router

from estimates.models import Room, Task, Topic
from estimates.schemas import RoomOutSchema, TaskListSchema

router = Router()


@router.post("/room")
async def create_room(request, payload: TaskListSchema):
    room = await Room.objects.acreate(name="New Room")
    for task_data in payload.tasks:
        task = await Task.objects.acreate(
            title=task_data.title, description=task_data.description
        )
        await Topic.objects.acreate(task=task, room=room)
    return {"public_name": room.public_name}


@router.get("/room/{public_name}", response=RoomOutSchema)
async def get_room(request, public_name: str):
    room = await Room.objects.aget(public_name=public_name)
    topics = await sync_to_async(list)(
        Topic.objects.filter(room=room).values("task__title", "task__description")
    )

    return {
        "name": room.name,
        "topics": topics,
    }
