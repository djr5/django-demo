from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(null=True, blank=True)
    emp_code = models.CharField(max_length=10)
    age = models.PositiveSmallIntegerField(default=25)
    phone = models.CharField(max_length=12)
    salary = models.FloatField(null=True, blank=True)

    def save(self, *args, ** kwargs):
        if not self.slug:
            self.slug = uuid.uuid4()
        return super().save( *args, ** kwargs)
    def __str__(self):
        return "{}-{}".format(self.user.first_name,self.user.last_name)


