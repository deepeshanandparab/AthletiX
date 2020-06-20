from datetime import date
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegistrationFrom, UserUpdateForm, ProfileUpdateForm
from .models import Tournament, Match, Scorecard, Team
from .resources import ScorecardResource, TeamResource
from tablib import Dataset


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
    team_player = Team.objects.filter(player=player)

    def tournaments_played(score_list):
        unique_list = []
        for tournament in score_list:
            if tournament not in unique_list:
                unique_list.append(tournament)
                print("len(unique_list)" ,len(unique_list))
            return len(unique_list)
        if len(unique_list) == 0:
            return 0

    if request.user.profile.birth_date:
        def age():
            today = date.today()
            birth_date = request.user.profile.birth_date
            return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

        context = {
            'score_list': score_list,
            'get_total_runs': get_total_runs(request.user),
            'batting_avg': calculate_batting_avg(request.user, get_total_runs(request.user), get_not_out(request.user)),
            'get_overall_strike_rate': get_overall_strike_rate(get_total_runs(request.user),
                                                               get_balls_faced(request.user)),
            'get_man_of_the_match': get_man_of_the_match(request.user),
            'get_hundreds_count': get_runs_milestone_count(request.user, 150, 100),
            'get_fifties_count': get_runs_milestone_count(request.user, 100, 50),
            'get_thirties_count': get_runs_milestone_count(request.user, 50, 30),
            'get_total_wickets': get_total_wickets(request.user),
            'get_fifer_count': get_wickets_milestone_count(request.user, 5),
            'get_economy_rate': get_overall_economy_rate(get_total_runs_conceded(request.user),
                                                         get_total_overs(request.user)),
            'tournaments_played': tournaments_played(score_list),
            'team_player': team_player,
            'title': 'Profile',
            'age': age()
        }
        return render(request, 'account/profile.html', context)
    else:
        def age():
            return None
        context = {
                    'score_list': score_list,
                    'get_total_runs': get_total_runs(request.user),
                    'batting_avg': calculate_batting_avg(request.user, get_total_runs(request.user), get_not_out(request.user)),
                    'get_overall_strike_rate': get_overall_strike_rate(get_total_runs(request.user), get_balls_faced(request.user)),
                    'get_man_of_the_match':get_man_of_the_match(request.user),
                    'get_hundreds_count': get_runs_milestone_count(request.user, 150, 100),
                    'get_fifties_count': get_runs_milestone_count(request.user, 100, 50),
                    'get_thirties_count': get_runs_milestone_count(request.user, 50, 30),
                    'get_total_wickets': get_total_wickets(request.user),
                    'get_fifer_count': get_wickets_milestone_count(request.user, 5),
                    'get_economy_rate':get_overall_economy_rate(get_total_runs_conceded(request.user), get_total_overs(request.user)),
                    'tournaments_played': tournaments_played(score_list),
                    'title': 'Profile',
                    'age': age()
                }
    return render(request, 'account/profile.html', context)

# -------------------------------------- Functions for Profile Page Data ----------------------------------------
def get_total_runs(user):
    score_list = Scorecard.objects.filter(player=user).order_by('-match')
    total_runs = 0
    index = 0
    while index < len(score_list):
        total_runs += score_list[index].runs_scored
        index += 1
    return total_runs


def get_balls_faced(user):
    score_list = Scorecard.objects.filter(player=user).order_by('-match')
    total_balls_faced = 0
    index = 0
    while index < len(score_list):
        total_balls_faced += score_list[index].balls
        index += 1
    return total_balls_faced


def get_overall_strike_rate(runs, balls):
    if not balls == 0:
        overall_strike_rate = (runs / balls)*100
    else:
        overall_strike_rate = 0
    return overall_strike_rate

def get_not_out(user):
    score_list = Scorecard.objects.filter(player=user, is_not_out=True).order_by('-match')
    return len(score_list)

def calculate_batting_avg(user, runs, not_out):
    score_list = Scorecard.objects.filter(player=user)
    if not not_out == len(score_list) and not_out <= len(score_list):
        batting_avg = runs / (len(score_list)-not_out)
        return batting_avg
    else:
        batting_avg = 0
        return batting_avg


def get_total_wickets(user):
    score_list = Scorecard.objects.filter(player=user).order_by('-match')
    total_wickets = 0
    index = 0
    while index < len(score_list):
        total_wickets += score_list[index].wickets
        index += 1
    return total_wickets


def get_total_runs_conceded(user):
    score_list = Scorecard.objects.filter(player=user).order_by('-match')
    total_runs_conceded = 0
    index = 0
    while index < len(score_list):
        total_runs_conceded += score_list[index].runs_conceded
        index += 1
    return total_runs_conceded


def get_total_overs(user):
    score_list = Scorecard.objects.filter(player=user).order_by('-match')
    total_overs = 0
    index = 0
    while index < len(score_list):
        total_overs += score_list[index].overs_bowled
        index += 1
    return total_overs


def get_overall_economy_rate(runs_conceded, overs_bowled):
    if overs_bowled > 0:
        overall_economy_rate = (runs_conceded / overs_bowled)
    else:
        overall_economy_rate = 0
    return overall_economy_rate


def get_man_of_the_match(user):
    score_list = Scorecard.objects.filter(player=user, man_of_the_match =True).order_by('-match')
    return score_list.count


def get_runs_milestone_count(user, milestone_ceiling_value, milestone_floor_value):
    score_list = Scorecard.objects.filter(player=user).order_by('-match')
    milestone_count = 0
    index = 0
    while index < len(score_list):
        if score_list[index].runs_scored < milestone_ceiling_value and score_list[index].runs_scored >= milestone_floor_value:
            milestone_count += 1
            index += 1
        return milestone_count

def get_wickets_milestone_count(user, milestone):
    score_list = Scorecard.objects.filter(player=user).order_by('-match')
    milestone_count = 0
    index = 0
    while index < len(score_list):
        if score_list[index].wickets >= milestone:
            milestone_count += 1
            index += 1
        return milestone_count





# -------------------------------------------------------------------------------------------------------------------

@login_required
def profile_update(request, id):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST or None, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile details updated successfully.')
            return redirect('profile', request.user.id)
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

    if request.method == "POST":
        scoresheet_resource = ScorecardResource()
        dataset = Dataset()
        new_scoresheet = request.FILES['datafile']

        if not new_scoresheet.name.endswith('xlsx'):
            messages.error(request, 'Please upload file with valid format')
            return render(request, 'account/my_stats.html')
        imported_data = dataset.load(new_scoresheet.read(), format='xlsx')
        for data in imported_data:
            value = Scorecard(
                    data[0],
                    data[1],
                    data[2],
                    data[3],
                    data[4],
                    data[5],
                    data[6],
                    data[7],
                    data[8],
                    data[9],
                    data[10],
                    data[11]
                )
            value.save()
        messages.success(request, 'Scoresheet uploaded successfully')
    context = { "score_list": score_list, "tournament_list": tournament_list, "title": "My Statistics"}
    return render(request, 'account/my_stats.html', context)

@login_required
def teams(request):
    team_list = Team.objects.all()
    print(f"T: {team_list}")

    if request.method == "POST":
        team_resource = TeamResource()
        dataset = Dataset()
        new_team = request.FILES['datafile']

        if not new_team.name.endswith('xlsx'):
            messages.error(request, 'Please upload file with valid format')
            return render(request, 'account/teams.html')
        imported_data = dataset.load(new_team.read(), format='xlsx')
        for data in imported_data:
            value = Team(
                    data[0],
                    data[1],
                    data[2]
                )
            value.save()
        messages.success(request, 'Team data uploaded successfully')
    context = {'team_list':team_list, 'title':'Teams'}
    return render(request, 'account/teams.html', context)