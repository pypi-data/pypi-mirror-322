from django.db import models
from django.contrib.auth.models import BaseUserManager

class ObjectManager(BaseUserManager):
    def get_queryset(self, fetch_action="active"):
        if fetch_action == "active":
            return super().get_queryset().filter(status_code=1)
        elif fetch_action == "inactive":
            return super().get_queryset().filter(status_code=0)
        elif fetch_action == "all":
            return super().get_queryset()

    def create_user(self, username, password=None):

        user = self.model(
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
       
        user = self.create_user(
            password=password,
            username=username
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class Base(models.Model):
    status_code = models.BooleanField(default=1)
    activity_status = models.IntegerField(default=1)
    created_by = models.PositiveIntegerField(null=False,blank=True)
    updated_by = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ObjectManager()

    class Meta:
        abstract = True