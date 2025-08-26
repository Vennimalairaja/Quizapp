from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Staff(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    email=models.EmailField(max_length=255)

class Questions(models.Model):
    Question=models.CharField(max_length=400)
    Option_a=models.CharField(max_length=300)
    Option_b=models.CharField(max_length=300)
    Option_c=models.CharField(max_length=300)
    Option_d=models.CharField(max_length=300)
    Correct_ans=models.CharField(max_length=300)
    def __str__(self):
        return self.Question


