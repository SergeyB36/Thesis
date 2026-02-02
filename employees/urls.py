from django.conf.urls.static import static
from rest_framework.routers import SimpleRouter

from config import settings
from employees.apps import EmployeesConfig
from employees.views import EmployeeViewSet

app_name = EmployeesConfig.name

router = SimpleRouter()
router.register("", EmployeeViewSet, basename="employee")

urlpatterns = []

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
