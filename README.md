DRF Any Permissions (AP)
========================
Django Rest Framework currently provides permssions as an all-or-nothing solution, which makes it difficult to use them with different authentication types.  AP allows you to get around that barrier by only requiring one permission to pass out of a group to access a view.

When would I need to use this?
==============================
* When you use multiple authentication types on a view.
* When you have different requirements for people to access a view, and only one needs to be met.

Is this on PyPi?
================
You can install this through PIP.  You must have Django Request Framework and
Django already, but the name implies that anyway.

```
pip install drf-any-permissions
```

You can also install it from source by cloning this repository using Git.

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

Multiple permissions
---------------------
If you specify a list of permissions, the list will be checked until one of them returns `True`, meaning that they have permission.  It will stop at the first one, so make sure that your views do not depend on the other permissions being processed.

Nested permissions
-----------------------------
AP only supports a single layer of nested permissions.  An example of this is shown in the examples section.  If you need anything more complex than that (2+ layers), we gladly accept pull requests that add it.  This allows you to "chain" permission checks together, which allows for you to require that two permissions out of two specific lists must be met before they can access the view.

Examples
========

AP has a few use cases, some which are more complex than others, so here are a few examples to show them.

One permission
--------------

```python
from rest_framework import permissions, viewsets
from rest_any_permissions import permissions

class ExmapleViewSet(viewsets.ModelViewSet):
    permission_classes = [AnyPermissions]
    any_permission_classes = permissions.DjangoModelPermissions
    model = ExampleModel
```

As stated above, this works the same as if the permission was inside of the `permission_classes` attribute.  If the permission fails that is specified in `any_permission_classes`, the user will be denied access.

There is no need for you to use AP in this case, but it is provided as a fallback.

Multiple permissions
--------------------

```python
from rest_framework import permissions, viewsets
from rest_any_permissions import permissions

class ExmapleViewSet(viewsets.ModelViewSet):
    permission_classes = [AnyPermissions]
    any_permission_classes = [permissions.DjangoModelPermissions, permissions.IsAdminUser]
    model = ExampleModel
```

AP will check a list of permissions to see which one passes.

* If the user has the permission as required by `DjangoModelPermissions`, they will be granted access to the view.  In this case, `IsAdminUser` is never checked.
* If the user does not have the permission as required by `DjangoModelPermissions`, they will be checked against `IsAdminUser`.  If they pass `IsAdminUser`, they will be granted access to the view.
* If the user fails both `DjangoModelPermissions` and `IsAdminUser`, the user will not be granted access to the view.

An example of where this would be used is if you were sharing an API across multiple applications.  They might require different authentication and have different ways of checking permissions.

Nested permissions
------------------

```python
from rest_framework import permissions, viewsets
from rest_any_permissions import permissions


class IsLucky(permissions.BasePermission):

    def has_permission(self, request, view):
        import random
        
        return random.randint(1, 10) > 8


class ExmapleViewSet(viewsets.ModelViewSet):
    permission_classes = [AnyPermissions]
    any_permission_classes = [
        [permissions.IsAdminUser, IsLucky],
        [permissions.DjangoModelPermissions, permissions.TokenHasReadWriteScope],
    ]
    model = ExampleModel
```

This situation assumes you have another permission that needs to be checked.  In our case, this is `IsLucky`, because everyone needs some randomness in their life.

This allows you to chain permissions, which is something you can't do without nesting permissions.  This is useful in situations where you would use `AnyPermissions` twice, which you can't do without nesting permissions.

When the request comes through, the permissions are checked in order.

* If `IsAdminUser` passes, `IsLucky` is never checked.  The process would then continue.
* If `IsAdminUser` fails, `IsLucky` is called.  If it fails, the user is not given access to the view.  If it passes, the process continues.

Assuming that the process continues, the next list of permissions would be checked:

* If `DjangoModelPermissions` passes, `TokenHasReadWriteScope` is never checked.  This would allow you to use the same API for your main application as you would for external applications, making it DRY.
* If `DjangoModelPermissions` fails, `TokenHasReadWriteScope` is checked.  If it passes, the user will be granted access to the view.  If it fails, the user would be denied access to the API, even though they passed the first check.

An example of where this would be used in a project is if you needed to use the same API for external applications as you used on your main website.  You would also need a second condition that needed to be met, which makes this use case somewhat rare.

Contributing
============
If you see something that needs to be fixed, send us a pull request.  If you don't feel like fixing it, or are not sure how to go about it, create an [issue on GitHub](https://github.com/kevin-brown/drf-any-permissions/issues) about it and we can work it out.

Tests
-----
Pull requests (for features) won't be accepted without tests.  You can run the test suite with:
```
python runtests.py
```
