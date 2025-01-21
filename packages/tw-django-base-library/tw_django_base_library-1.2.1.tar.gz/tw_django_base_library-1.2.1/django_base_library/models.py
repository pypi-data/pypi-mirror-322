from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, Group, Permission, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField

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


import re

# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):

    # default user fields do not alter
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(blank=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    groups = models.ManyToManyField(Group,blank=True)
    user_permissions = models.ManyToManyField(Permission, blank=True)
    is_staff = models.BooleanField(default=0)
    is_superuser = models.BooleanField(default=0)

    mobile = PhoneNumberField(blank=True)
    '''
    JSON format for the address. This format is changed according to the need of the project
    {
        "line1":"",
        "line2":"",
        "area":"",
        "city":"",
        "landmark":"",
        "state":"",
        "pincode":"",
        "country":""
    }

    How to filter through the address: 
    If you have to filter city: 
    User.objects.filter(address__city="<CITY_NAME>").all()
    Here, city is the key in the address json

    '''
    address = models.JSONField(null=True,blank=True)
    profile_img = models.ImageField(upload_to='profile_img/', null=True, blank=True)
    status = models.BooleanField(default=1)
    activity_status = models.IntegerField(default=1)
    created_by = models.PositiveIntegerField(default=1)
    updated_by = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  
    unique_id = models.CharField(unique=True, max_length=20, null=True, blank=True)
    
    objects = ObjectManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
    

    def save(self, *args, **kwargs):


        # TO BE IMPLEMENTED FOR UNIQUE FIELDS
        if self.status == False:

            if  not re.search("_deleted_", self.username):
                
                count = 0
    
                while True:

                    username = f"{self.username}_deleted_{count}"
                    if User.objects.get_queryset('all').filter(username=username).exists():
                        count += 1
                        continue
                    else:
                        break

                self.username = username

        super(User, self).save(*args, **kwargs)

class Privileges(Base):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Roles(Base):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    privileges = models.ManyToManyField(Privileges)
   
    def __str__(self):
        return self.name
   
class UserRoleAssociation(Base):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    role = models.ForeignKey(Roles, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.user.username} : {self.role.name}"
    
