from django.db import models

# Create your models here.
class Questions(models.Model):
    Question=models.CharField(max_length=400)
    Option_a=models.CharField(max_length=300)
    Option_b=models.CharField(max_length=300)
    Option_c=models.CharField(max_length=300)
    Option_d=models.CharField(max_length=300)
    Correct_ans=models.CharField(max_length=300)
    def __str__(self):
        return Question