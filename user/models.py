from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password, role, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set!")
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, role=role, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, password, role, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, first_name, last_name, password, role, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    DEVELOPER = 'developer'
    PROJECT_MANAGER = 'project manager'
    ROLE_CHOICES = [
        (DEVELOPER, 'Developer'),
        (PROJECT_MANAGER, 'Project Manager'),
    ]

    email = models.EmailField(unique=True, verbose_name=_("Email"))
    first_name = models.CharField(max_length=255, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=255, verbose_name=_("Last Name"))
    role = models.CharField(choices=ROLE_CHOICES, max_length=255, verbose_name=_("Role"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    is_staff = models.BooleanField(default=False, verbose_name=_("Is Staff"))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'users'
        indexes = [models.Index(fields=['email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff', ])]

    def __str__(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    @property
    def is_developer(self):
        return self.role == User.DEVELOPER

    @property
    def is_project_manager(self):
        return self.role == User.PROJECT_MANAGER
