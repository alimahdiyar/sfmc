from django.contrib import admin
from .models import CompetitionField, Manager, Participant, Team, PTR, UploadedFile
# Register your models here.

admin.site.register(CompetitionField)
admin.site.register(Manager)
admin.site.register(Participant)
admin.site.register(Team)
admin.site.register(PTR)
admin.site.register(UploadedFile)
