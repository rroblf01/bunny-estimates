from django.contrib import admin

from estimates.models import Room, Task, Topic, Vote

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Task)
admin.site.register(Vote)
