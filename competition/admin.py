from django.contrib import admin
from .models import CompetitionField, Participant, Team
# Register your models here.

admin.site.register(CompetitionField)
admin.site.register(Participant)
admin.site.register(Team)