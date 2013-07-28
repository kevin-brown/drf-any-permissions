from django.test import TestCase
from django.test.client import RequestFactory
from rest_framework.permissions import BasePermission
from rest_framework.views import APIView
from rest_any_permissions.permissions import AnyPermissions


class TruePermission(BasePermission):
    
    def has_permission(self):
        return True


class FalsePermission(BasePermission):
    
    def has_permission(self):
        return False


class PermissionsTest(TestCase):
    
    def setUp(self):
        self.requests = RequestFactory()
    
    def test_no_permissions(self):
        pass
    
    def test_default_passed(self):
        class DefaultApiView(APIView):
            permission_classes = [AnyPermissions]
            any_permission_classes = [TruePermission]
        
        view = DefaultApiView()
        request = self.requests.get("/")
        
        self.assertEqual(None, view.check_permissions(request))
    
    def test_default_failed(self):
        class DefaultApiView(APIView):
            permission_classes = [AnyPermissions]
            any_permission_classes = [FalsePermission]
        
        view = DefaultApiView()
        request = self.requests.get("/")
        
        self.assertEqual(None, view.check_permissions(request))
    
    def test_single_permission(self):
        pass
    
    def test_multiple_permissions(self):
        pass
    
    def test_chained_permissions(self):
        pass
