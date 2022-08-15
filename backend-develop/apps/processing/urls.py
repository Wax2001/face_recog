from django.urls import path, include
from apps.processing.views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'records', RecordViewSet, basename='records')

urlpatterns = [
    path('api/', include(router.urls)),
    ]