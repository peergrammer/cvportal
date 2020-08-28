from django import forms
from django.contrib.auth.models import User
from .models import Profile, Education, Attachment

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Must be unique'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Provide a valid email'}),
        }
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords dont match.')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('marital_status', 'dependents', 'years_experience', 'date_of_birth', 'nationality',
                    'residence_country', 'residence_city', 'mobile_number')
        widgets = {
            'marital_status': forms.Select(attrs={'class': 'form-control'}),
            'dependents':  forms.NumberInput(attrs={'class': 'form-control'}),
            'years_experience': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.25'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your citizenship'}),
            'residence_country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Current country you are in'}),
            'residence_city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Current city you are in'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E.164 Format (ex. +639991234567'}),
        }

class EducationEditForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ('degree_title', 'university', 'gpa')
        widgets = {
            'degree_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bachelor\'s Degree' }),
            'university':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'College or University'}),
            'gpa': forms.NumberInput(attrs={'class': 'form-control','step': '0.01'}),
        }

class AttachmentEditForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ('attachment_name', 'attachment_file')
        widgets = {
            'attachment_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Display name' }),
            'attachment_file': forms.FileInput(attrs={'class': 'form-control-file' }),
        }
