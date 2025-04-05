from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from pi3back.occurrences.models import Classroom

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    
class User(AbstractUser):

    username = None

    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True, max_length=255)
    is_professor = models.BooleanField(default=False)
    is_aluno = models.BooleanField(default=False)
    is_responsavel = models.BooleanField(default=False)
    responsavel = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        if self.pk:
            if self.is_aluno:
                classrooms = Classroom.objects.filter(members = self)
                if classrooms.exists():
                    classroom = classrooms.first()
                    classroom.members.remove(self)
                    classroom.save()
        super().save(*args, **kwargs)


