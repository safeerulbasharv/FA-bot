from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class FacultyUser(AbstractUser):
    # Add your custom fields here if any
    groups = models.ManyToManyField(Group, related_name="facultyuser_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="facultyuser_permissions", blank=True)
