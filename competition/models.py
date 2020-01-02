from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class CompetitionField (models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    team_member_limit = models.IntegerField()

    def __str__(self):
        return self.name

class Manager (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    student_card_image = models.ImageField()
    university = models.CharField(max_length=50)

    def __str__(self):
        return self.first_name + " " + self.last_name + " " + self.phone_number

class Participant (models.Model):
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    student_card_image = models.ImageField()
    university = models.CharField(max_length=50)

    def __str__(self):
        return self.first_name + " " + self.last_name + " " + self.phone_number


class Team (models.Model):
    name = models.CharField(max_length=100)
    competition_field = models.ForeignKey(CompetitionField, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class PTR (models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.team.name + self.participant.first_name + self.participant.last_name

class UploadedFile (models.Model):
    team = models.ForeignKey(Team, on_delete=models.PROTECT)
    upload_date = models.DateTimeField(auto_now_add=True)
