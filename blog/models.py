from django.db import models


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=16)
    dob = models.DateField()
    current_occupation = models.CharField(max_length=32)


class JobPost(models.Model):
    title = models.CharField(max_length=16)
    job_desc = models.TextField(max_length=500)
    date_posted = models.DateTimeField()
    deadline = models.DateField()


class Applications(models.Model):
    pass
