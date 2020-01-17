from django.db import models
from django.contrib.auth.models import User


def student_card_image_upload_location(instance, filename):
    print(filename)
    return "participant/%s/student_card.%s" % (instance.name, filename.split('.')[-1])


def national_card_image_upload_location(instance, filename):
    print(filename)
    return "participant/%s/national_card.%s" % (instance.name, filename.split('.')[-1])


# Create your models here.

class TeamTypeConsts:
    PARTICIPANT = '0'
    PUBLIC_STUDENT = '1'
    PUBLIC_ORGANIZATION = '2'

    states = (
        (PARTICIPANT, "شرکت کنندگان در مسابقه"),
        (PUBLIC_STUDENT, "آزاد دانشجویی"),
        (PUBLIC_ORGANIZATION, "آزاد سازمانی"),
    )


class CompetitionField(models.Model):
    needs_adviser = models.BooleanField(default=True)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    team_member_limit_min = models.IntegerField()
    team_member_limit_max = models.IntegerField()

    def __str__(self):
        return self.name


class Participant(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.PROTECT, related_name="profile")

    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

    student_card_image = models.ImageField(upload_to=student_card_image_upload_location,
                                           null=True,
                                           blank=True,
                                           width_field="student_card_height_field",
                                           height_field="student_card_width_field")
    student_card_height_field = models.IntegerField(default=0, null=True)
    student_card_width_field = models.IntegerField(default=0, null=True)

    national_card_image = models.ImageField(upload_to=national_card_image_upload_location,
                                            null=True,
                                            blank=True,
                                            width_field="national_card_height_field",
                                            height_field="national_card_width_field")
    national_card_height_field = models.IntegerField(default=0, null=True)
    national_card_width_field = models.IntegerField(default=0, null=True)

    university = models.CharField(max_length=255, null=True, blank=True)
    organization = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name + " " + self.phone_number


class Adviser(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    university = models.CharField(max_length=255)


class Team(models.Model):
    manager = models.ForeignKey(Participant, null=True, blank=True, on_delete=models.PROTECT, related_name="teams")
    adviser = models.OneToOneField(Adviser, null=True, blank=True, on_delete=models.PROTECT, related_name="team")
    participants = models.ManyToManyField(Participant, blank=True, related_name="participant_teams")
    team_type = models.CharField(max_length=1, choices=TeamTypeConsts.states)
    name = models.CharField(max_length=100, blank=True, null=True)
    competition_field = models.ForeignKey(CompetitionField, on_delete=models.CASCADE,  blank=True, null=True)

    upload_date = models.DateTimeField(null=True, blank=True)
    uploaded_file = models.FileField(null=True, blank=True)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.manager.name
