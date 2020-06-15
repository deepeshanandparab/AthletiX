from datetime import date
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegistrationFrom, UserUpdateForm, ProfileUpdateForm
from .models import Tournament, Match, Scorecard


def register(request):
    if request.method == 'POST':
        form = RegistrationFrom(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            messages.success(request, f'Account created for {username} successfully !')
            return redirect('login-page')
        else:
            messages.error(request, f'Error Occurred ! Please check all the fields.')
    else:
        form = RegistrationFrom()
    return render(request, 'account/register.html', {'form': form})


@login_required
def profile(request, player):
    score_list = Scorecard.objects.filter(player=player).order_by('-match')
    print(f"score_list : {len(score_list)}")

    if request.user.profile.birth_date:
        def age():
            today = date.today()
            birth_date = request.user.profile.birth_date
            return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        context = {'title': 'Profile', 'age': age()}
    else:
        def age():
            return None
        context = {'score_list': score_list, 'get_total_runs': get_total_runs(request.user), 'title': 'Profile', 'age': age()}
    return render(request, 'account/profile.html', context)

def get_total_runs(user):
    score_list = Scorecard.objects.filter(player=user).order_by('-match')
    total_runs = 0
    index = 0
    while index < len(score_list):
        total_runs += score_list[index].runs_scored
        print(f"total_runs : {total_runs}")
        index += 1
    return total_runs

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

@login_required
def my_stats(request, player):
    score_list = Scorecard.objects.filter(player=player).order_by('-match')
    tournament_list = Tournament.objects.all()
    context = { "score_list": score_list, "tournament_list": tournament_list, "title": "My Statistics"}
    return render(request, 'account/my_stats.html', context)

@login_required
def teams(request):
    context = {"title":"Teams"}
    return render(request, 'account/teams.html', context)