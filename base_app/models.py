import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


def generate_uuid():
    return uuid.uuid4().hex  # 'asdawdsdwadadasdasawda'


class ApplicationUser(AbstractUser):
    user_id = models.CharField(
        max_length=32, primary_key=True, unique=True, default=generate_uuid
    )
    phone_no = models.CharField(max_length=12)
    profile_picture = models.ImageField(upload_to="uploads/", null=True, blank=True)
    is_renter = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)


class RenterUser(models.Model):
    renter_id = models.CharField(
        max_length=32, primary_key=True, unique=True, default=generate_uuid
    )
    application_user = models.ForeignKey(ApplicationUser, on_delete=models.CASCADE)


class AdminUser(models.Model):
    admin_id = models.CharField(
        max_length=32, primary_key=True, unique=True, default=generate_uuid
    )
    application_user = models.ForeignKey(ApplicationUser, on_delete=models.CASCADE)


class BaseClass(models.Model):
    reference_id = models.CharField(
        max_length=32, primary_key=True, unique=True, default=generate_uuid
    )
    data_generated_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class RenterRegisterRequests(BaseClass):
    application_user = models.ForeignKey(ApplicationUser, on_delete=models.CASCADE)
    is_reviewed = models.BooleanField(default=False)


class RenterRegisterResults(BaseClass):
    renter_request = models.ForeignKey(RenterRegisterRequests, on_delete=models.CASCADE)
    reviewed_by = models.ForeignKey(AdminUser, on_delete=models.CASCADE)
    is_approved = models.BooleanField()
