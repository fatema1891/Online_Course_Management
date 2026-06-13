# from django.contrib.auth.models import AbstractUser
# from django.db import models

# class CustomUser(AbstractUser):
#     ROLE_CHOICES = (
#         ('student', 'Student'),
#         ('teacher', 'Teacher'),
#         ('admin', 'Admin'),
#     )
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
#     email = models.EmailField(unique=True)
    
#     def __str__(self):
#         return f"{self.username} ({self.get_role_display()})"
        


# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom user model with a role field.
    Roles:
        - 'admin': administrator (same as superuser)
        - 'teacher': teacher
        - 'student': student
    """
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    
    # Use email as an additional unique field (optional)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

    # Helper methods to check role
    def is_student(self):
        return self.role == 'student'

    def is_teacher(self):
        return self.role == 'teacher'

    def is_admin(self):
        return self.role == 'admin' or self.is_superuser