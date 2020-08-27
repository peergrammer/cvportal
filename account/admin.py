from django.contrib import admin
from .models import Profile, Education, Attachment, Country, City

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'nationality', 'date_of_birth']
    
@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['user', 'degree_title', 'university', 'gpa']

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'attachment_name', 'attachment_file']

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_prefix']

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['country', 'name']