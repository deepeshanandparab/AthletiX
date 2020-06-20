from import_export import resources
from .models import Scorecard, Team

class ScorecardResource(resources.ModelResource):
    class meta:
        model = Scorecard

class TeamResource(resources.ModelResource):
    class meta:
        model = Team