import datetime
from apps.processing.models import *

from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework import permissions
from apps.processing.serializers import RecordSerializer, UserApproveSerializer, NotApprovedUsersSerializer

from rest_framework.response import Response

from apps.processing import logger


class UserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.filter(available=True, is_approved=False).order_by('id')
    serializer_class = NotApprovedUsersSerializer
    action_serializers = {
        'list': NotApprovedUsersSerializer,
        'approve': UserApproveSerializer,
    }
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            return self.action_serializers.get(self.action, self.serializer_class)
        return super(UserViewSet, self).get_serializer_class()

    def get_queryset(self):
        users_with_images = []
        for user in User.objects.filter(available=True, is_approved=False):
            if user.images.exists():
                users_with_images.append(user)
        return users_with_images

    @action(detail=True, url_path='approve', name='approve', methods=['post'], permission_classes=[permissions.AllowAny], serializer_class=[UserApproveSerializer])
    def approve(self, request):
        serializer = UserApproveSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = self.get_object()
            if user:
                user.is_approved = True
                user.save()
                return Response(data={'user': user.id, 'is_approved': user.is_apprvoed}, status=status.HTTP_200_OK)
        return Response('Could not approve the user', status=status.HTTP_400_BAD_REQUEST)


    
class RecordViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows records to be viewed or edited.
    """
    queryset = Record.objects.filter(available=True).order_by('obj_created_date')
    serializer_class = RecordSerializer
    permission_classes = [permissions.AllowAny]

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