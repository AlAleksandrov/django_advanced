from django.contrib.auth import get_user_model
from django.db import models
from todos.choices import TodoStateChoice

UserModel = get_user_model()


# Create your models here.
class Category(models.Model):
    name = models.CharField(
        max_length=15,
    )

    def __str__(self):
        return self.name


class Todo(models.Model):
    title = models.CharField(
        max_length=50,
    )
    description = models.TextField(
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='todos',
    )
    state = models.BooleanField(
        choices=[
            (True, TodoStateChoice.DONE),
            (False, TodoStateChoice.NOT_DONE)
        ],
        default=False,
    )
    assignees = models.ManyToManyField(
        UserModel,
        related_name='assignees_todos',
        blank=True
    )

    def __str__(self):
        return self.title