from django.contrib import admin
from .models import Profile, Tournament, Match, Scorecard, Team

admin.site.register(Profile)
admin.site.register(Tournament)
admin.site.register(Match)
admin.site.register(Scorecard)
admin.site.register(Team)
