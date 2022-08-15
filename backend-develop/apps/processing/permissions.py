from ipaddress import ip_address
from rest_framework import permissions
from config import env

class AllowedIPsPermission(permissions.BasePermission):
    """
    Global permission to check for allowance of incoming IP Address.
    """
    def has_permission(self, request, view):
        ip_addr = request.META['REMOTE_ADDR']
        if str(ip_addr) in (env('ALLOWED_IPs')).split(','):
            return True
        return False