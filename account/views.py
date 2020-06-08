from datetime import date

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import RegistrationFrom, UserUpdateForm, ProfileUpdateForm

def register(request):
    if request.method == 'POST':
        form = RegistrationFrom(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username} successfully !')
            return redirect('login-page')
        else:
            messages.error(request, f'Error Occurred ! Please check all the fields.')
    else:
        form = RegistrationFrom()
    return render(request, 'account/register.html', {'form': form})


@login_required
def profile(request):
    def age():
        today = date.today()
        birth_date = request.user.profile.birth_date
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    context = {'title': 'Profile', 'age': age()}
    return render(request, 'account/profile.html', context)


@login_required
def profile_update(request, id):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST or None, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile details updated successfully.')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'title': 'Update Profile'
    }

    return render(request, 'account/update_profile.html', context)