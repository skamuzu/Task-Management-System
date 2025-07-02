from django.db import models
from django.db.models import Manager
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from uuid import uuid4
from django.db.models import constraints, Deferrable


class CustomUserManager(Manager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    username = models.CharField(max_length=30, blank=True, default="User")
    email = models.EmailField(unique=True)
    picture = models.ImageField(upload_to="images/")
    created = models.DateTimeField(auto_now_add=True)

    class RoleChoices(models.TextChoices):
        ADMIN = ("Admin",)
        EMPLOYEE = "Employee"

    role = models.CharField(choices=RoleChoices)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class AdminManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=CustomUser.RoleChoices.ADMIN)


class Admin(CustomUser):
    class Meta:
        proxy = True

    objects = AdminManager()


class EmployeeManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=CustomUser.RoleChoices.EMPLOYEE)


class Employee(CustomUser):
    class Meta:
        proxy = True

    objects = EmployeeManager()


class AdminProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)


class Department(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    name = models.CharField(max_length=40)
    owner = models.ForeignKey(AdminProfile, on_delete=models.CASCADE)
    color = models.CharField(max_length=40)
    
class EmployeeProfile(models.Model):
    employee = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    employer = models.ForeignKey(AdminProfile, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)





        
