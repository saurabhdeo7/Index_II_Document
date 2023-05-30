# django_project/users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):

    STATUS = (
        ('valuer', 'valuer'),
        ('admin', 'admin'),
    )

    email = models.EmailField(unique=True)
    status = models.CharField(max_length=100, choices=STATUS, default='valuer')
    # description = models.TextField("Description", max_length=600, default='', blank=True)
    state=models.CharField("State", max_length=50,blank=True , default='')
    city=models.CharField("City", max_length=50,blank=True, default='')
    number_of_docs_uploaded = models.IntegerField(default=0)
    number_of_docs_downloded = models.IntegerField(default=0)

    def __str__(self):
        return self.username

class GuestUser(models.Model):
    Firstname=models.CharField( "First name", max_length=50,blank=True, default='')
    Lastname= models.CharField("Last name", max_length=50,blank=True, default='')
    email= models.EmailField("Email", max_length=254, blank=False, default='')
    state=models.CharField("State", max_length=50,blank=True, default='')
    city=models.CharField("City", max_length=50,blank=True, default='')
    
    def __str__(self):
        return self.Firstname +" "+ self.Lastname
    