from django.contrib import admin
from .models import CompetitionField, Participant, Team, Adviser
# Register your models here.

class TeamAdmin(admin.ModelAdmin):
    list_display = ['team_name', 'field_or_type', 'payment_done']
    list_filter = ['competition_field']

class AdviserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'university']

class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone_number']

admin.site.register(CompetitionField)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Adviser, AdviserAdmin)