from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Users, Project, Task, Comment
from .serializers import UserSerializer, ProjectSerializer, TaskSerializer, CommentSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from datetime import datetime
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404



@api_view(['POST'])
def register_user(request):
    """
    Registers a new user.
    
    Parameters:
        - username: The username of the new user (string)
        - email: The email address of the user (string)
        - password: The password of the user (string)
        - first_name: The first name of the user (string)
        - last_name: The last name of the user (string)
    
    Response:
        - 201: User created successfully
        - 400: Bad request if validation fails
    """
    try:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = Users()
            user.username = request.data.get("username", "")
            user.email = request.data.get("email", "")
            user.password = make_password(request.data.get("password"))
            user.first_name = request.data.get("first_name", "")
            user.last_name = request.data.get("last_name", "")
            user.date_joined = datetime.now()
            user.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_user(request):
    """
    Logs a user in and provides access and refresh tokens.
    
    Parameters:
        - username: The username of the user (string)
        - password: The password of the user (string)
    
    Response:
        - 200: Tokens provided if login is successful
        - 400: Invalid credentials if login fails
    """
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = get_object_or_404(Users, username=username)

        if user and check_password(password, user.password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'login_status': "User successfully logged in"
            })
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'Error': 'Invalid Method'}, status=status.HTTP_404_NOT_FOUND)
    
    
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def user_details(request, id):
    """
    Retrieves, updates, partially updates, or deletes a user.
    
    Parameters:
        - id: The ID of the user (int)
    
    Response:
        - 200: User details returned or updated
        - 204: User deleted successfully
        - 400: Bad request if validation fails
        - 404: User not found
    """
    try:
        user = Users.objects.get(id=id)
        if request.method == 'GET':
            return Response(UserSerializer(user).data)
        elif request.method in ['PUT', 'PATCH']:
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            user.delete()
            return Response({'detail': 'Users deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'Error': 'Invalid Method'}, status=status.HTTP_404_NOT_FOUND)
    except Users.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def projects(request):
    """
    Retrieves all projects or creates a new project.
    
    Parameters:
        - description: Description of the project (string)
        - owner: ID of the user owning the project (int)
    
    Response:
        - 200: List of projects returned
        - 201: Project created successfully
        - 400: Bad request if validation fails
        - 404: User not found
    """
    if request.method == 'GET':
        projects = Project.objects.all()
        return Response(ProjectSerializer(projects, many=True).data)
    elif request.method == 'POST':
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            project = Project()
            project.description = request.data.get("description", "")
            owner = get_object_or_404(Users, id=request.data.get('owner'))
            if owner:
                project.owner = owner
            else:
                Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            project.created_at = datetime.now()
            project.save()
            return Response(ProjectSerializer(project).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'Error': 'Invalid Method'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET','PUT', 'PATCH', 'DELETE'])
def project_details(request, id):
    """
    Retrieves, updates, partially updates, or deletes a project.
    
    Parameters:
        - id: The ID of the project (int)
    
    Response:
        - 200: Project details returned or updated
        - 204: Project deleted successfully
        - 400: Bad request if validation fails
        - 404: Project not found
    """
    try:
        project = Project.objects.get(id=id)
        if request.method == 'GET':
            return Response(ProjectSerializer(project).data)
        elif request.method in ['PUT', 'PATCH']:
            serializer = ProjectSerializer(project, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            project.delete()
            return Response({'detail': 'Project deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'Error': 'Invalid Method'}, status=status.HTTP_404_NOT_FOUND)
    except Project.DoesNotExist:
        return Response({'detail': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def tasks(request, project_id):
    """
    Retrieves tasks for a specific project or creates a new task for a project.
    
    Parameters:
        - project_id: The ID of the project (int)
        - description: Description of the task (string)
        - assigned_to: ID of the user assigned to the task (int)
    
    Response:
        - 200: List of tasks returned
        - 201: Task created successfully
        - 400: Bad request if validation fails
        - 404: Project or user not found
    """
    try:
        project = Project.objects.get(id=project_id)
        if request.method == "GET":
            tasks = Task.objects.filter(project=project)
            return Response(TaskSerializer(tasks, many=True).data)
        elif request.method == "POST":
            serializer = TaskSerializer(data=request.data)
            if serializer.is_valid():
                assigned_to_id = request.data.get('assigned_to')
                assigned_to = None
                if assigned_to_id:
                    # Validate the assigned_to ID
                    try:
                        assigned_to = Users.objects.get(id=assigned_to_id)
                    except Users.DoesNotExist:
                        return Response({'detail': 'Assigned user not found'}, status=status.HTTP_400_BAD_REQUEST)
                serializer.save(project=project, assigned_to=assigned_to)
                return Response(TaskSerializer(serializer.instance).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'Error': 'Invalid Method'}, status=status.HTTP_404_NOT_FOUND)
    except Project.DoesNotExist:
        return Response({'detail': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def task_details(request, id):
    """
    Retrieves, updates, partially updates, or deletes a task.
    
    Parameters:
        - id: The ID of the task (int)
    
    Response:
        - 200: Task details returned or updated
        - 204: Task deleted successfully
        - 400: Bad request if validation fails
        - 404: Task not found
    """
    try:
        task = Task.objects.get(id=id)
        if request.method == "GET":
            return Response(TaskSerializer(task).data)
        elif request.method in ['PUT', 'PATCH']:
            serializer = TaskSerializer(task, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            task.delete()
            return Response({'detail': 'Task deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'Error': 'Invalid Method'}, status=status.HTTP_404_NOT_FOUND)
    except Task.DoesNotExist:
        return Response({'detail': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def comments(request, task_id):
    """
    Retrieves comments for a specific task or creates a new comment for a task.
    
    Parameters:
        - task_id: The ID of the task (int)
        - content: Content of the comment (string)
        - user: ID of the user who made the comment (int)
    
    Response:
        - 200: List of comments returned
        - 201: Comment created successfully
        - 400: Bad request if validation fails
        - 404: Task or user not found
    """
    try:
        task = Task.objects.get(id=task_id)
        if request.method == "GET":
            comments = Comment.objects.filter(task=task)
            return Response(CommentSerializer(comments, many=True).data)
        elif request.method == "POST":
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                comment = Comment()
                comment.content = request.data.get("content")
                print('request.data.get("content") >>>>> ', request.data.get("content"))
                user = get_object_or_404(Users, id=request.data.get("user"))
                if user:
                    comment.user = user
                else:
                    return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
                comment.task = get_object_or_404(Task, id=task_id)
                comment.save()
                return Response(CommentSerializer(serializer.instance).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'Error': 'Invalid Method'}, status=status.HTTP_404_NOT_FOUND)
    except Task.DoesNotExist:
        return Response({'detail': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def comment_details(request, id):
    """
    Retrieves, updates, partially updates, or deletes a comment.
    
    Parameters:
        - id: The ID of the comment (int)
    
    Response:
        - 200: Comment details returned or updated
        - 204: Comment deleted successfully
        - 400: Bad request if validation fails
        - 404: Comment not found
    """
    try:
        comment = Comment.objects.get(id=id)
        if request.method == "GET":
            return Response(CommentSerializer(comment).data)
        elif request.method in ['PUT', 'PATCH']:
            serializer = CommentSerializer(comment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            comment.delete()
            return Response({'detail': 'Comment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'Error': 'Invalid Method'}, status=status.HTTP_404_NOT_FOUND)
    except Comment.DoesNotExist:
        return Response({'detail': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
