from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# new imports
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

# Create your models here.


class SiteUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required.")
        if not password:
            raise ValueError("A password is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


STATUS = ((0, "DRAFT"), (1, "PUBLISH"))


class SiteUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("email address", unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = SiteUserManager()
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True)

    dob = models.DateField()
    current_occupation = models.CharField(max_length=32)
    # posts = models.ForeignKey(JobPost, on_delete=models.CASCADE)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.email


class JobPost(models.Model):
    title = models.CharField(max_length=16)
    job_content = models.TextField()
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    status = models.IntegerField(choices=STATUS, default=0)
    picture = models.ImageField(blank=True, null=True, upload_to="media/images")
    poster = models.ForeignKey(
        SiteUser, on_delete=models.CASCADE, related_name="job_post"
    )  # person who posted job
    deadline = models.DateField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(JobPost, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-created_on"]


"""class Applications(models.Model):
    user = models.ManyToManyField(User)
    # date = models.date"""
