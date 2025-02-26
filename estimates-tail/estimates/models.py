import uuid

from asgiref.sync import sync_to_async
from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=160)
    public_name = models.UUIDField(unique=True, default=uuid.uuid4)

    def __str__(self):
        return f"{self.name} ({self.public_name})"


class Task(models.Model):
    title = models.CharField(max_length=160)
    description = models.TextField()

    def __str__(self):
        return self.title


class Topic(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task.title} in {self.room.name}"

    @property
    async def average_votes(self):
        votes = await sync_to_async(list)(self.vote_set.all())

        if not votes:
            return None

        values = [vote.point_value for vote in votes if vote.point_value]
        return sum(values) / len(values)


class Vote(models.Model):
    POINT_CHOICES = [
        ("0", "0"),
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("5", "5"),
        ("8", "8"),
        ("13", "13"),
        ("21", "21"),
        ("34", "34"),
        ("55", "55"),
        ("89", "89"),
        ("?", "?"),
        ("Cafe", "Cafe"),
    ]

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    voter_name = models.CharField(max_length=160)
    point = models.CharField(max_length=4, choices=POINT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def point_value(self) -> int | None:
        return int(self.point) if self.point.isdigit() else None

    def __str__(self):
        return f"{self.voter_name} voted {self.point} for {self.topic.task.title}"
