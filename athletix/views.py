from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect

from athletix import settings
from athletix.forms import ContactForm


def homePage(request):
    context = {'title': 'Home'}
    return render(request, 'athletix/home.html', context)

def aboutPage(request):
    context = {'title':'About'}
    return render(request, 'athletix/about.html', context)

def contactPage(request):
    if request.method == 'GET':
        contact_form = ContactForm()
    else:
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            # ------------------------- Mail for Admin -------------------------
            subject_for_admin = contact_form.cleaned_data['subject']
            message_for_admin = 'Received an enquiry from : ' + contact_form.cleaned_data['email'] + '\n' \
                                                                                             'Enquiry Message : ' + \
                                contact_form.cleaned_data['message']
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [settings.EMAIL_HOST_USER]

            # ------------------------- Mail for User -------------------------
            subject_for_user = contact_form.cleaned_data['subject']
            message_for_user = 'Hi ' + contact_form.cleaned_data['email'] + '. Warm welcome from AthletiX support team.' \
                                                                    'We have got your query and we will soon reply to you with proper answer.' \
                                                                    'Thanks again for being such a fantastic customer! \n\nCheers!!!\n[from Admin]'
            admin_email = settings.EMAIL_HOST_USER
            user_recipient_list = [contact_form.cleaned_data['email']]
            try:
                send_mail(subject_for_admin, message_for_admin, from_email, recipient_list)
                send_mail(subject_for_user, message_for_user, admin_email, user_recipient_list)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            messages.success(request, 'Mail has been sent successfully.')
            return redirect('home-page')
    return render(request, 'athletix/contact.html', {'contact_form': contact_form, 'title': 'Contact Us'})