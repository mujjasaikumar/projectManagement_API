from django.contrib import admin
from .models import Users, Project, ProjectMember, Task, Comment

admin.site.register(Users)
admin.site.register(Project)
admin.site.register(ProjectMember)
admin.site.register(Task)
admin.site.register(Comment)
