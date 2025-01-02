from django.urls import path
from . import views
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="TechForing API",
        default_version='v1',
        description="API documentation for the project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="your_email@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('api/users/register/', views.register_user, name='register_user'),
    path('api/users/login/', views.login_user, name='login_user'),
    path('api/users/<int:id>/', views.user_details, name='user_details'),
    path('api/projects/', views.projects, name='projects'),
    path('api/projects/<int:id>/', views.project_details, name='project_details'),
    path('api/projects/<int:project_id>/tasks/', views.tasks, name='tasks'),
    path('api/tasks/<int:id>/', views.task_details, name='task_details'),
    path('api/tasks/<int:task_id>/comments/', views.comments, name='comments'),
    path('api/comments/<int:id>/', views.comment_details, name='comment_details'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
