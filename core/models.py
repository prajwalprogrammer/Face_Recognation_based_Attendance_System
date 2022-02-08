# from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    # first_name1 = models.CharField(null=True, blank="ddd",max_length=70)
    # last_name1 = models.CharField(null=True, blank="ddf",max_length=70)
    prn = models.BigIntegerField(null=True,default=1212)
    year=models.CharField(null=True,max_length=6,choices=[('First', 'First'),
    ('Second', 'Second'),('Third', 'Third'),('Fourth', 'Fourth')])
    sem=models.CharField(null=True,max_length=6,choices=[('I', 'I'),('II', 'II')])
    phone = models.BigIntegerField(null=True,default=000000000)
    # email = models.EmailField(null=True)
    # birthday=models.DateField(null=True)
    gender=models.CharField(null=True,max_length=6,choices=[('Male', 'Male'),
    ('Female', 'Female')])
    image = models.ImageField(upload_to='Student_profile',null=True)


    def __str__(self):
        return self.user.username
