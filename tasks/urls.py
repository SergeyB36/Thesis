from django.conf.urls.static import static
from django.urls import path

from config import settings
from tasks.apps import TasksConfig
from tasks.views import (
    CriticalTaskListAPIView,
    GetTaskAPIView,
    TaskCreateAPIView,
    TaskDestroyAPIView,
    TaskListAPIView,
    TaskRetrieveAPIView,
    TaskUpdateAPIView,
    WarningTaskListAPIView,
)

app_name = TasksConfig.name

urlpatterns = [
    path("create/", TaskCreateAPIView.as_view(), name="task-create"),
    path("", TaskListAPIView.as_view(), name="task-list"),
    path("<int:pk>/", TaskRetrieveAPIView.as_view(), name="task-retrieve"),
    path("<int:pk>/delete/", TaskDestroyAPIView.as_view(), name="task-delete"),
    path("<int:pk>/update/", TaskUpdateAPIView.as_view(), name="task-update"),
    path("get_task/", GetTaskAPIView.as_view(), name="get-task"),
    path("critical_task/", CriticalTaskListAPIView.as_view(), name="critical-task-list"),
    path("warning_task/", WarningTaskListAPIView.as_view(), name="warning-task-list"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
