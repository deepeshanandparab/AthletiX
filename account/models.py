from datetime import date

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    )

    HAND_CHOICES = (
        ('left', 'Left'),
        ('right', 'Right')
    )

    BATTING_ORDER_CHOICES = (
        ('opener' , 'Opener'),
        ('middle', 'Middle Order'),
        ('finish', 'Finisher'),
        ('tail', 'Tail Ender')
    )

    BOWLING_TYPE_CHOICES = (
        ('RAF', 'Right Arm Fast'),
        ('RAM', 'Right Arm Medium'),
        ('LAF', 'Left Arm Fast'),
        ('LAM', 'Left Arm Medium'),
        ('RAFS', 'Right Arm Finger Spin'),
        ('RAWS', 'Right Arm Wrist Spin'),
        ('LAFS', 'Left Arm Finger Spin'),
        ('LAWS', 'Left Arm Wrist Spin')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Not Mentioned', null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    batting_hand = models.CharField(max_length=5, choices=HAND_CHOICES, default='Not Mentioned', null=True, blank=True)
    batting_order = models.CharField(max_length=6, choices=BATTING_ORDER_CHOICES, default='Not Mentioned', null=True, blank=True)
    bowling_hand = models.CharField(max_length=5, choices=HAND_CHOICES, null=True, default='Not Mentioned', blank=True)
    bowling_type = models.CharField(max_length=5, choices=BOWLING_TYPE_CHOICES, default='Not Mentioned', null=True, blank=True)
    image = models.ImageField(default='default.png', upload_to='profile_pictures')

    def __str__(self):
        return f'{self.user.username} Profile'

    def getAge(self):
        today = date.today()
        birth_date = self.user.profile.birth_date
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))


class Tournament(models.Model):
    MATCH_TYPE = (
        ('50', '50 Overs'),
        ('20', '20 Overs'),
        ('10', '10 Overs'),
        ('35', '35 Overs'),
        ('90', '90 Overs'),
        ('test5', '5 Days Test'),
        ('test3', '3 Days Test')
    )

    AGE_GROUP = (
        ('u10','Under 10'),
        ('u12', 'Under 12'),
        ('u14', 'Under 14'),
        ('u16', 'Under 16'),
        ('u19', 'Under 19'),
        ('u23', 'Under 23'),
        ('open', 'Open Age'),
    )

    tournament_name = models.CharField(max_length=50)
    age_group = models.CharField(max_length=6, choices=AGE_GROUP, default='', null=True, blank=True)
    venue = models.CharField(max_length=20, default='')
    place = models.CharField(max_length=20, default='')
    start_date = models.DateField()
    end_date = models.DateField()
    match_type = models.CharField(max_length=5, choices=MATCH_TYPE,  default='', null=True, blank=True)
    total_teams = models.IntegerField()
    winner = models.CharField(max_length=50, null=True, blank=True)
    runner_up = models.CharField(max_length=50, null=True, blank=True)
    best_batsman = models.CharField(max_length=50, null=True, blank=True)
    best_bowler = models.CharField(max_length=50, null=True, blank=True)
    best_fielder = models.CharField(max_length=50, null=True, blank=True)
    best_player = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'Tournament - {self.tournament_name}'


class Match(models.Model):
    MATCH_TYPE = (
        ('50', '50 Overs'),
        ('20', '20 Overs'),
        ('10', '10 Overs'),
        ('35', '35 Overs'),
        ('90', '90 Overs'),
        ('test5', '5 Days Test'),
        ('test3', '3 Days Test')
    )

    match_date = models.DateField()
    venue = models.CharField(max_length=20, default='')
    place = models.CharField(max_length=20, default='')
    match_type = models.CharField(max_length=5, choices=MATCH_TYPE, default='', null=True, blank=True)
    tournament = models.ForeignKey(Tournament, null=True, blank=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.match_type} Match at {self.venue} on {self.match_date}'

class Scorecard(models.Model):
    player = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    runs_scored = models.IntegerField(default=0)
    balls = models.IntegerField(default=0)
    fours = models.IntegerField(default=0)
    sixes = models.IntegerField(default=0)
    is_not_out = models.BooleanField(default=0)
    overs_bowled = models.IntegerField(default=0)
    runs_conceded = models.IntegerField(default=0)
    wickets = models.IntegerField(default=0)
    man_of_the_match = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.player}\'s score on match played at {self.match.venue}, {self.match.place}'

    def getStrikeRate(self):
        if not self.balls == 0:
            strike_rate = (self.runs_scored / self.balls)*100
            return round(strike_rate,2)
        else:
            return 0

    def getEconomyRate(self):
        if not self.overs_bowled == 0:
            economy_rate = (self.runs_conceded / self.overs_bowled)
            return round(economy_rate,2)
        else:
            return 0

class Team(models.Model):
    POSITION_CHOICES = (
        ('pl11', 'Playing 11'),
        ('sub', 'Substitutes'),
        ('prob', 'Probables')
    )

    player = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    position = models.CharField(max_length=6, choices=POSITION_CHOICES, default='')

    def __str__(self):
        return f'{self.player} is in {self.position}'









