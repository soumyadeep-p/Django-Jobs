from django.db import models
from users.models import User

class Resume(models.Model):
    title_choices = (
        ('Developer', 'Developer'),
        ('Consultant','Consultant'),
        ('Analyst' , 'Analyst'),
        ('Manager' , 'Manager'),
        ('UI/UX' , 'UI/UX'),
        ('Human Resource' , 'Human Resource'),
        ('Operations' , 'Operations')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length = 100, null = True, blank = True)
    surname = models.CharField(max_length = 100, null = True, blank = True)
    location = models.CharField(max_length = 100, null = True, blank = True)
    title = models.CharField(max_length=100, choices = title_choices, null = True, blank = True)
    upload_resume = models.FileField(upload_to='uploaded_resumes/', null = True, blank = True)

    def __str__(self):
        return f'{self.first_name} {self.surname}'