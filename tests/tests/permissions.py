from django.test import TestCase
from django.test.client import RequestFactory
from rest_framework.permissions import BasePermission
from rest_framework.views import APIView
from rest_any_permissions.permissions import AnyPermissions


class TestView(APIView):

    def test_permission(self, request):
        from rest_framework.request import Request

        request = Request(request)

        self.request = request

        for permission in self.get_permissions():
            if not permission.has_permission(request, self):
                return False

        return True


class TruePermission(BasePermission):

    def has_permission(self, request, view):
        return True


class FalsePermission(BasePermission):

    def has_permission(self, request, view):
        return False


class PermissionsTest(TestCase):

    def setUp(self):
        self.requests = RequestFactory()

    def test_no_permissions(self):
        class DefaultApiView(TestView):
            permission_classes = [AnyPermissions]

        view = DefaultApiView()
        request = self.requests.get("/")

        self.assertFalse(view.test_permission(request))

    def test_single_permission_flat(self):
        class DefaultApiView(TestView):
            permission_classes = [AnyPermissions]
            any_permission_classes = TruePermission

        view = DefaultApiView()
        request = self.requests.get("/")

        self.assertTrue(view.test_permission(request))

    def test_single_permission_passed(self):
        class DefaultApiView(TestView):
            permission_classes = [AnyPermissions]
            any_permission_classes = [TruePermission]

        view = DefaultApiView()
        request = self.requests.get("/")

        self.assertTrue(view.test_permission(request))

    def test_single_permission_failed(self):
        class DefaultApiView(TestView):
            permission_classes = [AnyPermissions]
            any_permission_classes = [FalsePermission]

        view = DefaultApiView()
        request = self.requests.get("/")

        self.assertFalse(view.test_permission(request))

    def test_multiple_permissions_passed(self):
        class DefaultApiView(TestView):
            permission_classes = [AnyPermissions]
            any_permission_classes = [TruePermission, FalsePermission]

        view = DefaultApiView()
        request = self.requests.get("/")

        self.assertTrue(view.test_permission(request))

    def test_multiple_permissions_passed_any_order(self):
        class DefaultApiView(TestView):
            permission_classes = [AnyPermissions]
            any_permission_classes = [FalsePermission, TruePermission]

        view = DefaultApiView()
        request = self.requests.get("/")

        self.assertTrue(view.test_permission(request))

    def test_multiple_permissions_failed(self):
        class DefaultApiView(TestView):
            permission_classes = [AnyPermissions]
            any_permission_classes = [FalsePermission, FalsePermission]

        view = DefaultApiView()
        request = self.requests.get("/")

        self.assertFalse(view.test_permission(request))

    def test_chained_permissions(self):
        class DefaultApiView(TestView):
            permission_classes = [AnyPermissions]
            any_permission_classes = [
                [TruePermission, FalsePermission],
                TruePermission,
            ]

        view = DefaultApiView()
        request = self.requests.get("/")

        self.assertTrue(view.test_permission(request))

    def test_chained_first_failed(self):
        class DefaultApiView(TestView):
            permission_classes = [AnyPermissions]
            any_permission_classes = [
                FalsePermission,
                [TruePermission, FalsePermission],
            ]

        view = DefaultApiView()
        request = self.requests.get("/")

        self.assertFalse(view.test_permission(request))

    def test_chained_late_failed(self):
        class DefaultApiView(TestView):
            permission_classes = [AnyPermissions]
            any_permission_classes = [
                [TruePermission, FalsePermission],
                FalsePermission,
            ]

        view = DefaultApiView()
        request = self.requests.get("/")

        self.assertFalse(view.test_permission(request))
