from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    MARITAL_STATUS_CHOICES = [('s','Single'), ('m','Married'),]
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS_CHOICES)
    dependents = models.PositiveSmallIntegerField(null=True)
    years_experience = models.PositiveSmallIntegerField(null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=75)
    residence_country = models.CharField(max_length=75)
    residence_city = models.CharField(max_length=150)
    mobile_number = models.CharField(max_length=16)
    def __str__(self):
        return self.user.username

class Education(models.Model):
    user = models.ForeignKey(Profile,
                                on_delete=models.CASCADE)
    degree_title = models.CharField(max_length=150)
    university = models.CharField(max_length=150)
    gpa = models.DecimalField(max_digits=3, decimal_places=2)
    def __str__(self):
        return self.degree_title

class Attachment(models.Model):
    user = models.ForeignKey(Profile,
                                on_delete=models.CASCADE)
    attachment_name = models.CharField(max_length=150)
    attachment_file = models.FileField(upload_to='users/%y/%m/%d/')
    def __str__(self):
        return self.attachment_name


