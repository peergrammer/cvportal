from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm, EducationEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile, Education, Attachment
import logging

logger = logging.getLogger(__name__)

@login_required
def panel(request):
    user_profile = get_object_or_404(Profile, user=request.user)
    user_education = Education.education_entries.all().filter(user=request.user)
    user_attachment = Attachment.attachment_entries.filter(user=request.user)
    return render(request, 'account/panel.html', {  'section': 'panel', 
                                                    'user_profile': user_profile, 
                                                    'user_education': user_education,
                                                    'user_attachment': user_attachment})

def profile_detail(request):
    user_profile_detail = get_object_or_404(Profile, user=request.user)
    return render(request, 'account/panel.html', {'section': 'panel', 'user_profile_detail': user_profile_detail})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        logger.info("@register POST -- after the user submmitted the create account")
        if user_form.is_valid():
            new_user = user_form.save(commit=False) #dont commit yet
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            # Create the profile,and education associated with this registration
            Profile.objects.create(user=new_user)
            Education.objects.create(user=new_user)
            Attachment.objects.create(user=new_user)
            # Send an email to the user
            send_email_to_new_user(user_form.cleaned_data)
            sent = True
            return render(request, 'account/register_done.html', {'new_user': new_user})
        else:
            logger.error("Error in POST")
    else:
        logger.debug("a new signup page")
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        logger.info(request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                        data=request.POST)
        logger.info("-s profile request post")
        logger.info(request.POST)
        logger.info("-e profile request post")
        education_form = EducationEditForm(instance=request.user,
                                        data=request.POST)
        if user_form.is_valid() and profile_form.is_valid() and education_form.is_valid():
            user_form.save()
            profile_form.save()
            education_form.save()
            logger.info("forms are saved.")
        else:
            logger.error("Edit profile ERROR in post!")
        return panel(request)
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        education_form = EducationEditForm(instance=request.user)

    return render(request, 'account/edit.html', 
                    {   'user_form': user_form, 
                        'profile_form': profile_form,
                        'education_form': education_form
                    })

def send_email_to_new_user(cleaned_data):
    subject = f"Welcome {cleaned_data['first_name']} {cleaned_data['last_name']} to CV Portal"
    message = f"You are now a registered user. Your username is {cleaned_data['username']}"
    send_mail(subject, message, 'admin@cvportal.com',[cleaned_data['email']])
    logger.info("email sent")
