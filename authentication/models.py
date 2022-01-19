from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField

from authentication.helpers import UserManager


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        default=timezone.now, db_index=True,
        verbose_name=_('Created At'))
    modified_at = models.DateTimeField(
        auto_now=True, db_index=True,
        verbose_name=_('Modified At'))

    class Meta:
        abstract = True


class User(AbstractUser, BaseModel):
    first_name = models.CharField(max_length=254,
                                  verbose_name=_('First Name'),
                                  null=True, blank=True)
    last_name = models.CharField(max_length=254,
                                 verbose_name=_('Last Name'),
                                 null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True,
                              db_index=True)
    country = CountryField(null=True,
                           blank=True, multiple=False)
    USERNAME_FIELD = settings.AUTH_USERNAME_FIELD
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return "{}-{} {}".format(self.first_name,
                                 self.last_name, self.email)
