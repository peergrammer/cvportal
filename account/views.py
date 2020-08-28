from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm, EducationEditForm, AttachmentEditForm
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
    sent = False
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        logger.info("@register POST -- after the user submmitted the create account")
        if user_form.is_valid():
            new_user = user_form.save(commit=False) #dont commit yet
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            # Create the profile associated with this registration
            Profile.objects.create(user=new_user)
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
        logger.info(request.POST)
        education_form = EducationEditForm(data=request.POST)
        attachment_form = AttachmentEditForm(data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid() and education_form.is_valid():
            user_form.save()
            profile_form.save()
            # for the education table
            new_education = education_form.save(commit=False)
            new_education.user = request.user
            new_education.save()
            # for the attachment table
            new_attachment = attachment_form.save(commit=False)
            new_attachment.user = request.user
            new_attachment.save()
            logger.info("forms are saved.")
            # Send an email to the user
            send_email_to_user_after_profile_update(user_form.cleaned_data)
        else:
            logger.error("Edit profile ERROR in post!")
        return panel(request)
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        education_form = EducationEditForm(instance=request.user)
        attachment_form = AttachmentEditForm(instance=request.user)

    return render(request, 'account/edit.html', 
                    {   'user_form': user_form, 
                        'profile_form': profile_form,
                        'education_form': education_form,
                        'attachment_form': attachment_form
                    })

@login_required
def education_post(request):
    if request.method == 'POST':
        education_form = EducationEditForm(data=request.POST)
        if education_form.is_valid():
            # create the education record
            new_education = education_form.save(commit=False)
            new_education.user = request.user
            new_education.save()
        return panel(request)
    else:
        education_form = EducationEditForm()
    
    return render(request, 'account/education.html',{'education_form': education_form})

@login_required
def attachment_post(request):
    if request.method == 'POST':
        logger.info("---Attachement POST")
        logger.info(request.POST)
        attachment_form = AttachmentEditForm(data=request.POST, files=request.FILES)
        if attachment_form.is_valid():
            # create the attachment record
            new_attachment = attachment_form.save(commit=False)
            new_attachment.user = request.user
            new_attachment.save()
        #return panel(request)
    else:
        attachment_form = AttachmentEditForm()
    
    return render(request, 'account/attachment_upload.html',{'attachment_form': attachment_form})

def send_email_to_new_user(cleaned_data):
    subject = f"Welcome {cleaned_data['first_name']} {cleaned_data['last_name']} to CV Portal"
    message = f"You are now a registered user. Your username is {cleaned_data['username']}"
    send_mail(subject, message, 'admin@cvportal.com',[cleaned_data['email']])
    logger.info("send_email_to_new_user - email sent")

def send_email_to_user_after_profile_update(cleaned_data):
    subject = f"Profile Update Notification {cleaned_data['first_name']} {cleaned_data['last_name']}"
    message = f"Your profile has been updated. This is a generated message."
    send_mail(subject, message, 'admin@cvportal.com',[cleaned_data['email']])
    logger.info("send_email_to_user_after_profile_update - email sent")
