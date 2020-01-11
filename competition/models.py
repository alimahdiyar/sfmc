from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class TeamTypeConsts():
    
    TYPE_1 = '0'
    TYPE_2 = '1'

    states = (
        (TYPE_1, "ثبت نام شرکت کنندگان در مسابقه"),
        (TYPE_2, "ثبت نام آزاد (خارج از مسابقه)"),
    )

class CompetitionField(models.Model):
    name = models.CharField(max_length=100)
    can_free_register = models.BooleanField(default=True)
    price = models.IntegerField()
    team_member_limit_min = models.IntegerField()
    team_member_limit_max = models.IntegerField()

    def __str__(self):
        return self.name


class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    student_card_image = models.ImageField()
    university = models.CharField(max_length=50)

    def __str__(self):
        return self.first_name + " " + self.last_name + " " + self.phone_number


class Team(models.Model):
    manager = models.ForeignKey(Participant, on_delete=models.CASCADE,
                                related_name="teams")  # redundant for development speed
    team_type = models.CharField(max_length=1, choices=TeamTypeConsts.states)
    name = models.CharField(max_length=100)
    competition_field = models.ForeignKey(CompetitionField, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class UploadedFile(models.Model):
    team = models.ForeignKey(Team, on_delete=models.PROTECT)
    upload_date = models.DateTimeField(auto_now_add=True)
    uploaded_file = models.FileField()
