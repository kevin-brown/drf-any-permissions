from rest_framework.permissions import BasePermission


class AnyPermissions(BasePermission):

    def get_permissions(self, view):
        """
        Get all of the permissions that are associated with the view.
        """

        permissions = getattr(view, "any_permission_classes", [])

        if not hasattr(permissions, "__iter__"):
            permissions = [permissions]

        return permissions

    def has_permission(self, request, view):
        """
        Check the permissions on the view.
        """

        permissions = self.get_permissions(view)

        if not permissions:
            return False

        for perm_class in permissions:
            if hasattr(perm_class, "__iter__"):
                classes = perm_class

                for perm_class in classes:
                    permission = perm_class()

                    if permission.has_permission(request, view):
                        break
                    else:
                        return False
            else:
                permission = perm_class()

                if permission.has_permission(request, view):
                    return True

        return False

    def has_object_permission(self, request, view, obj):
        """
        Check the object permissions on the view.
        """

        permissions = self.get_permissions(view)

        if not permissions:
            return False

        for perm_class in permissions:
            if hasattr(perm_class, "__iter__"):
                classes = perm_class

                for perm_class in classes:
                    permission = perm_class()

                    if permission.has_object_permission(request, view, obj):
                        break
                    else:
                        return False
            else:
                permission = perm_class()

                if permission.has_object_permission(request, view, obj):
                    return True

        return False
