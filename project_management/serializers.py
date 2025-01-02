from rest_framework import serializers
from .models import Users, Project, ProjectMember, Task, Comment
from rest_framework import serializers
from .models import Users


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'date_joined']


class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'created_at']

class ProjectMemberSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = ProjectMember
        fields = ['id', 'project', 'user', 'role']

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority', 'assigned_to', 'project', 'created_at', 'due_date']
        read_only_fields = ['project', 'created_at']
        
class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    task = TaskSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'task', 'created_at']





















# from rest_framework import serializers
# from .models import Users, Project, ProjectMember, Task, Comment

# # Users Serializer
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Users
#         fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']

# # Project Serializer
# class ProjectSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Project
#         fields = ['id', 'name', 'description', 'owner', 'created_at']

# # ProjectMember Serializer
# class ProjectMemberSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProjectMember
#         fields = ['id', 'project', 'user', 'role']

# # Task Serializer
# class TaskSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Task
#         fields = ['id', 'title', 'description', 'status', 'priority', 'assigned_to', 'project', 'created_at', 'due_date']

# # Comment Serializer
# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = ['id', 'content', 'user', 'task', 'created_at']


























# from rest_framework import serializers
# from .models import Users, Project, Task, Comment

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Users
#         fields = ['id', 'username', 'email', 'password']
#         extra_kwargs = {'password': {'write_only': True}}

# class ProjectSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Project
#         fields = ['id', 'name', 'description', 'created_at']

# class TaskSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Task
#         fields = ['id', 'title', 'description', 'status', 'project', 'created_at']

# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = ['id', 'content', 'task', 'created_at']

