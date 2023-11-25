from collections.abc import Iterable
from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils.translation import gettext as _
from django.utils import timezone
import uuid


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("username", email.split("@")[0])
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("username", email.split("@")[0])
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    class Gender(models.TextChoices):
        male = "M"
        female = "F"

    class Role(models.TextChoices):
        agent = "AGENT"
        user = "USER"

    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False) 
    username = models.CharField(_("username"), max_length=30)
    email = models.EmailField(_("email address"), unique=True,)
    date_joined = models.DateTimeField(default=timezone.now)
    gender = models.CharField(_("Gender"), max_length=4, blank=True, null=True, choices=Gender.choices)
    role = models.CharField(_("Who are you?"), max_length=8, blank=True, null=True, choices=Role.choices)
    is_staff = models.BooleanField(default=False)
    objects = CustomUserManager()
    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    def absolute_url(self):
        return reverse('flash-detail', args=(self.id,))

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"