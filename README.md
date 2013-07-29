DRF Any Permissions (AP)
========================

Django Rest Framework currently provides permssions as an all-or-nothing solution, which makes it difficult to use them with different authentication types.  AP allows you to get around that barrier by only requiring one permission to pass out of a group to access a view.

When would I need to use this?
==============================
* When you use multiple authentication types on a view.
* When you have different requirements for people to access a view, and only one needs to be met.

How do I use this?
==================
On your View or ViewSet, you must include the permission `AnyPermissions`.

```python
from rest_framework import viewsets
from rest_any_permissions.permissions import AnyPermissions

class ExmapleViewSet(viewsets.ModelViewSet):
    permission_classes = [AnyPermissions]
    model = ExampleModel
```

From there you can specify the list of permissions that are needed through the `any_permission_classes` attribute.

```python
from rest_framework import permissions, viewsets
from rest_any_permissions import permissions

class ExmapleViewSet(viewsets.ModelViewSet):
    permission_classes = [AnyPermissions]
    any_permission_classes = [permissions.DjangoModelPermissions, permissions.IsAdminUser]
    model = ExampleModel
```

This can be a single permission class, a list of permission classes, or a list of list of permission classes.  AP handles these situations differently, so keep it in mind when you are specifying the permissions.

One permission
--------------
If you specify one permission, it will act as though it was a list with only one permission.  This means that is is essentially required, and it would be more useful had it been placed in the original list of required permissions.

A list of permissions
---------------------
If you specify a list of permissions, the list will be checked until one of them returns `True`, meaning that they have permission.  It will stop at the first one, so make sure that your views do not depend on the other permissions being processed.

A list of list of permissions
-----------------------------
AP only supports a single layer of nested lists.  If you need anything more complex than that, we gladly accept pull requests.  This allows you to "chain" permission checks together, which allows for you to require that two permissions out of two specific lists must be met before they can access the view.

Contributing
============
If you see something that needs to be fixed, send us a pull request.  If you don't feel like fixing it, or are not sure how to go about it, create an [issue on GitHub](https://github.com/kevin-brown/drf-any-permissions/issues) about it and we can work it out.

Tests
-----
Pull requests (for features) won't be accepted without tests.  You can run the test suite with:
```
python runtests.py
```