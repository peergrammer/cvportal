from django.db import models
from django.conf import settings

class ProfileManager(models.Manager):    
    def get_queryset(self):        
        return super(ProfileManager, self).get_queryset()

class EducationManager(models.Manager):    
    def get_queryset(self):        
        return super(EducationManager, self).get_queryset()

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    MARITAL_STATUS_CHOICES = [('s','Single'), ('m','Married'),]
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS_CHOICES)
    dependents = models.PositiveSmallIntegerField(null=True)
    years_experience = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=75)
    residence_country = models.CharField(max_length=75)
    residence_city = models.CharField(max_length=150)
    mobile_number = models.CharField(max_length=16)

    objects = models.Manager() # The default manager.
    profile_entries = ProfileManager() # Our custom manager.
    
    def __str__(self):
        return self.user.username

class Education(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    degree_title = models.CharField(max_length=150)
    university = models.CharField(max_length=150)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, null=True)

    objects = models.Manager() # The default manager.
    education_entries = EducationManager() # Our custom manager.

    def __str__(self):
        return self.degree_title

class Attachment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    attachment_name = models.CharField(max_length=150)
    attachment_file = models.FileField(upload_to='users/%y/%m/%d/')
    def __str__(self):
        return self.attachment_name

# enable this when it is required that the countries are required
# currently javascript in checking the relationship of countries and cities

class Country(models.Model):
    name = models.CharField(max_length=75)
    phone_prefix = models.CharField(max_length=4) 
    def __str__(self):
        return self.name

class City(models.Model):
    country = models.ForeignKey(Country,
                                on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    def __str__(self):
        return self.name
