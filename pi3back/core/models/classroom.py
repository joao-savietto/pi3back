from django.db import models

class Classroom(models.Model):
    
        name = models.CharField(max_length=255)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        members = models.ManyToManyField('users.User', related_name='classrooms', blank=True)
    
        class Meta:
            ordering = ['name']