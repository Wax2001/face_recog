from django.urls import path, include
from apps.processing.views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'records', RecordViewSet, basename='records')

urlpatterns = [
    path('', DashboardListView.as_view(), name='home'),
    path("dashboard/", DashboardListView.as_view(), name="dashboard"),
    path("employees/", EmployeesListView.as_view(), name="employees"),
    path("reports/", ReportsListView.as_view(), name="reports"),
    path('api/', include(router.urls)),
    ]