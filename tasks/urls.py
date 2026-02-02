from django.conf.urls.static import static
from django.urls import path

from config import settings
from tasks.apps import TasksConfig
from tasks.views import (
    TaskCreateAPIView,
    TaskDestroyAPIView,
    TaskListAPIView,
    TaskRetrieveAPIView,
    TaskUpdateAPIView,
)

app_name = TasksConfig.name

urlpatterns = [
    path("create/", TaskCreateAPIView.as_view(), name="task-create"),
    path("", TaskListAPIView.as_view(), name="task-list"),
    path("<int:pk>/", TaskRetrieveAPIView.as_view(), name="task-retrieve"),
    path("<int:pk>/delete/", TaskDestroyAPIView.as_view(), name="task-delete"),
    path("<int:pk>/update/", TaskUpdateAPIView.as_view(), name="task-update"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
