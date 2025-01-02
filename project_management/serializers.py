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
