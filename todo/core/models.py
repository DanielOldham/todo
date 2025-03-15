from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Todo(models.Model):
    """
    Django model.
    Details one specific Todo item belonging to a User.
    """

    class TodoStatus(models.TextChoices):
        """
        Enumerates the 2 possible states of a Todo.
        """
        PENDING = 'P', _('Pending')
        COMPLETED = 'C', _('Completed')

    title = models.CharField(max_length=255, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    notes = models.TextField(blank=True, default='')
    status = models.CharField(max_length=1, choices=TodoStatus, default=TodoStatus.PENDING, blank=False, null=False)
