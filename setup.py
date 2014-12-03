
from setuptools import setup, find_packages

setup(
    name="django-multiselect",
    version="1.6.2",
    description="Django multiselect",
    author="Matt Morrison and Aaron Madison",
    include_package_data=True,
    zip_safe=False,
    packages=find_packages(exclude=['example*']),
    install_requires=open('requirements/dist.txt').read().split('\n'),
)
