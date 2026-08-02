from django.db import models
from django.contrib.auth.models import User


class EmployeeProfile(models.Model):
    ROLE_CHOICES = [
        ('root',     'Root'),
        ('admin',    'Admin'),
        ('editor',   'Editor'),
        ('author',   'Author'),
        ('reviewer', 'Reviewer'),
        ('viewer',   'Viewer'),
    ]
    ROLE_HIERARCHY = {
        'root': 100, 'admin': 80, 'editor': 60,
        'author': 40, 'reviewer': 20, 'viewer': 0,
    }

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='viewer')

    def __str__(self):
        return f'{self.user.username} - {self.get_role_display()}'

    def _level(self):
        return self.ROLE_HIERARCHY.get(self.role, 0)

    def has_role_at_least(self, min_role: str) -> bool:
        return self._level() >= self.ROLE_HIERARCHY.get(min_role, 0)

    def is_root(self):     return self.role == 'root'
    def is_admin(self):    return self.has_role_at_least('admin')
    def is_editor(self):   return self.has_role_at_least('editor')
    def is_author(self):   return self.has_role_at_least('author')
    def is_reviewer(self): return self.has_role_at_least('reviewer')
    def can_delete(self):  return self.has_role_at_least('admin')
    def can_publish(self): return self.has_role_at_least('reviewer')
    def can_create(self):  return self.has_role_at_least('author')
    def can_edit(self):    return self.has_role_at_least('author')
