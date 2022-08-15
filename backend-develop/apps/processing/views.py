import datetime
from django.views.generic import ListView
from apps.processing.models import *

from rest_framework import serializers, views, viewsets, status
from rest_framework import permissions
from apps.processing.serializers import RecordSerializer, UserSerializer
from rest_framework.authentication import BaseAuthentication, TokenAuthentication

from rest_framework.response import Response

from apps.processing import logger

class HomepageListView(ListView):
    template_name = 'index.html'
    model = Record

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        records = Record.objects.filter(available=True).order_by('-id')
        users = User.objects.filter(available=True).order_by('-id')
        context = {
            'records': records,
            'users': users,
        }
        return context

class DashboardListView(ListView):
    template_name = 'dashboard.html'
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = User.objects.exclude(working_hours=None, salary=None)
        n_users = User.objects.filter(available=True).count()
        n_reports = Record.objects.filter(available=True).count()

        avg_work_hours = self.compute_avg_work_hours(users, users.count())
        avg_hourly_rate = self.compute_avg_hourly_rate(users, users.count())

        late_arrived_users = Record.objects.exclude(late_arrive_time=None)
        early_left_users = Record.objects.exclude(early_leave_time=None)

        context = {
            'users': users,
            'n_users': n_users,
            'n_reports': n_reports,
            'avg_work_hours': avg_work_hours,
            'avg_hourly_rate': avg_hourly_rate,
            'late_reports': late_arrived_users,
            'early_reports': early_left_users, 
            }
        logger.info(f'{n_users}')
        return context

    def compute_avg_work_hours(self, users=None, n_users=1):
        logger.info(f'users considered in stats: {users}')
        # logger.info(f'users considered in stats: {(lambda users: (user.id for user in users))}')
        total_hours = 0
        for user in users:
            total_hours += user.salary.total_work_hours
        if n_users == 0:
            n_users = 1
        return '{:.1f}'.format(float(total_hours/n_users))

    def compute_avg_hourly_rate(self, users=None, n_users=1):
        total_rate = 0
        for user in users:
            total_rate += user.salary.hourly_rate
        if n_users == 0:
            n_users = 1
        return '{:.1f}'.format(float(total_rate/n_users))


class EmployeesListView(ListView):
    template_name = 'employees.html'
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = User.objects.filter(available=True).order_by('id')
        context = {'users': users}
        return context

class ReportsListView(ListView):
    template_name = 'reports.html'
    model = Record
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        records = Record.objects.filter(available=True).order_by('-obj_created_date')
        context = {'reports': records}
        return context


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.filter(available=True).order_by('id')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [BaseAuthentication, TokenAuthentication]

    
class RecordViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows records to be viewed or edited.
    """
    queryset = Record.objects.filter(available=True).order_by('obj_created_date')
    serializer_class = RecordSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        logger.info(request.data)
        logger.info(type(request.data))

        logger.info(serializer)

        data = request.data

        try:
            if isinstance(type(request.data), dict):
                if data['post_data'] == 'check-in':
                    self.perform_create(serializer)
                elif data['post_data'] == 'check-out':
                    if Record.objects.filter(user=data['user'], obj_created_date=datetime.datetime.now().date()).exists():
                        record = Record.objects.filter(user=data['user'], obj_created_date=datetime.datetime.now().date()).first()
                        record.check_out_time = data['check_out_time']
                        record.save()
            else:
                self.perform_create(serializer)
        except Exception as e:
            logger.error(f'error on record creation: {e}') 

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)