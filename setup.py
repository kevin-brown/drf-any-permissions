from setuptools import setup, find_packages
from rest_any_permissions import __version__
import os


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths}


setup(
    name="drf-any-permissions",
    version=__version__,
    url="https://github.com/kevin-brown/drf-any-permissions/",
    license="MIT",
    description="Permissions don't have to be all or nothing anymore, make "
                "integrating different authentication types easier.",
    author="Kevin Brown",
    author_email="kbrown@rediker.com",
    packages=find_packages(exclude=["tests*", ]),
    package_data=get_package_data("rest_any_permissions"),
    install_requires=[
        "Django>=1.3",
        "djangorestframework"
    ]
)
