from django.db import models
from django.conf import settings
from django_countries.fields import CountryField

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    MARITAL_STATUS_CHOICES = [('S','Single'), ('M','Married'),]
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS_CHOICES)
    dependents = models.PositiveSmallIntegerField(null=True)
    years_experience = models.PositiveSmallIntegerField(null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=75)
    residence_country = models.CharField(max_length=75)
    residence_city = models.CharField(max_length=150)
    mobile_number = models.CharField(max_length=16)

    #education one or more
        # degree title, university, gpa
    #attachment one or more
        #attachment_name (doc, pdf)


