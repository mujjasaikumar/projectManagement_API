from django.db import models


class Users(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_joined = models.DateTimeField(auto_now_add=True)


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="owned_projects")
    created_at = models.DateTimeField(auto_now_add=True)

class ProjectMember(models.Model):
    ROLE_CHOICES = [('Admin', 'Admin'), ('Member', 'Member')]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="projects")
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)


class Task(models.Model):
    STATUS_CHOICES = [('To Do', 'To Do'), ('In Progress', 'In Progress'), ('Done', 'Done')]
    PRIORITY_CHOICES = [('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')]

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES)
    assigned_to = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()


class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="comments")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)




































# from django.db import models
# from django.contrib.auth.models import AbstractUser

# class Users(AbstractUser):
#     date_joined = models.DateTimeField(auto_now_add=True)

#     # Fix the conflict with the default groups and user_permissions fields
#     groups = models.ManyToManyField(
#         'auth.Group', 
#         related_name='custom_user_set',  # Custom related_name for groups
#         blank=True
#     )
#     user_permissions = models.ManyToManyField(
#         'auth.Permission', 
#         related_name='custom_user_permissions_set',  # Custom related_name for user_permissions
#         blank=True
#     )

#     def __str__(self):
#         return self.username



# # Project Model
# class Project(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     owner = models.ForeignKey(Users, related_name="projects", on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name


# # Project Members Model (Associating Users to Projects with Roles)
# class ProjectMember(models.Model):
#     ADMIN = 'Admin'
#     MEMBER = 'Member'
#     ROLE_CHOICES = [
#         (ADMIN, 'Admin'),
#         (MEMBER, 'Member'),
#     ]

#     project = models.ForeignKey(Project, related_name="members", on_delete=models.CASCADE)
#     user = models.ForeignKey(Users, related_name="project_memberships", on_delete=models.CASCADE)
#     role = models.CharField(choices=ROLE_CHOICES, max_length=10)

#     def __str__(self):
#         return f"{self.user.username} - {self.project.name} ({self.role})"


# # Task Model
# class Task(models.Model):
#     TODO = 'To Do'
#     IN_PROGRESS = 'In Progress'
#     DONE = 'Done'
#     STATUS_CHOICES = [
#         (TODO, 'To Do'),
#         (IN_PROGRESS, 'In Progress'),
#         (DONE, 'Done'),
#     ]

#     LOW = 'Low'
#     MEDIUM = 'Medium'
#     HIGH = 'High'
#     PRIORITY_CHOICES = [
#         (LOW, 'Low'),
#         (MEDIUM, 'Medium'),
#         (HIGH, 'High'),
#     ]

#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     status = models.CharField(choices=STATUS_CHOICES, max_length=20, default=TODO)
#     priority = models.CharField(choices=PRIORITY_CHOICES, max_length=20, default=LOW)
#     assigned_to = models.ForeignKey(Users, related_name="tasks", on_delete=models.SET_NULL, null=True, blank=True)
#     project = models.ForeignKey(Project, related_name="tasks", on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     due_date = models.DateTimeField()

#     def __str__(self):
#         return self.title


# # Comment Model
# class Comment(models.Model):
#     content = models.TextField()
#     user = models.ForeignKey(Users, related_name="comments", on_delete=models.CASCADE)
#     task = models.ForeignKey(Task, related_name="comments", on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Comment by {self.user.username} on task {self.task.title}"
