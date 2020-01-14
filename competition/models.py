from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class TeamTypeConsts():
    
    TYPE_1 = '0'
    TYPE_2 = '1'
    TYPE_3 = '2'

    states = (
        (TYPE_1, "شرکت کنندگان در مسابقه"),
        (TYPE_2, "آزاد دانشجویی"),
        (TYPE_3, "آزاد سازمانی"),
    )


class CompetitionField(models.Model):
    needs_advisor = models.BooleanField(default=True)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    team_member_limit_min = models.IntegerField()
    team_member_limit_max = models.IntegerField()

    def __str__(self):
        return self.name


class Participant(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.PROTECT, related_name="profile")

    participant_team = models.ForeignKey('Team', on_delete=models.CASCADE,
                                related_name="members")
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    student_card_image = models.ImageField(null=True, blank=True)
    national_card_image = models.ImageField(null=True, blank=True)
    university = models.CharField(max_length=255, null=True, blank=True)
    organization = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name + " " + self.phone_number

class Advisor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    university = models.CharField(max_length=255)



class Team(models.Model):
    manager = models.OneToOneField(Participant, null=True, blank=True, on_delete=models.PROTECT, related_name="team")
    advisor = models.OneToOneField(Advisor, null=True, blank=True, on_delete=models.PROTECT, related_name="team")
    team_type = models.CharField(max_length=1, choices=TeamTypeConsts.states)
    name = models.CharField(max_length=100)
    competition_field = models.ForeignKey(CompetitionField, on_delete=models.CASCADE)
    
    upload_date = models.DateTimeField(null=True, blank=True)
    uploaded_file = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.name
