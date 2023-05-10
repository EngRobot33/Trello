from django.db import models
from django.utils.translation import gettext_lazy as _

from user.models import User


class Project(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    managers = models.ManyToManyField(User, related_name='manager', verbose_name=_('Managers'))
    developers = models.ManyToManyField(User, related_name='developer', verbose_name=_('Developers'))

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        db_table = 'project'
        indexes = [models.Index(fields=['title', 'description', ])]

    def __str__(self):
        return self.title


class Task(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    description = models.TextField(verbose_name=_('Description'))
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks', verbose_name=_('Project'))
    assignees = models.ManyToManyField(User, related_name='tasks', verbose_name=_('Assignees'))

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        db_table = 'tasks'
        indexes = [models.Index(fields=['title', 'description', 'project', ])]

    def __str__(self):
        return self.title
