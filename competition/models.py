from django.db import models
from django.contrib.auth.models import User



# Create your models here.
from django.db.models.signals import post_save

from invoice.models import Invoice


class TeamTypeConsts:
    PARTICIPANT = '0'
    PUBLIC_STUDENT = '1'
    PUBLIC_ORGANIZATION = '2'

    states = (
        (PARTICIPANT, "شرکت کنندگان در مسابقه"),
        (PUBLIC_STUDENT, "آزاد دانشجویی"),
        (PUBLIC_ORGANIZATION, "آزاد سازمانی"),
    )


def student_card_image_upload_location(instance, filename):
    return "participant/%s/student-card.%s" % (instance.name, filename.split('.')[-1])


def national_card_image_upload_location(instance, filename):
    return "participant/%s/national-card.%s" % (instance.name, filename.split('.')[-1])


def team_uploaded_file_upload_location(instance, filename):
    file_ext = filename.split('.')[-1]
    file_name = ''.join(filename.split('.')[:-1])
    return "team/%s/%s-%s.%s" % ((instance.name if instance.name else instance.manager.name), file_name, str(instance.upload_date.strftime('%Y-%m-%d-%H-%M-%S')), file_ext)


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

    @property
    def invoice_items(self):
        if not self.teams.exists():
            return []
        team_type = self.teams.first().team_type
        
        if team_type == TeamTypeConsts.PUBLIC_STUDENT:
            return [{
                'title': 'ثبت نام آزاد دانشجویی',
                'price': 100000
            }]
        elif team_type == TeamTypeConsts.PUBLIC_ORGANIZATION:
            return [{
                'title': 'ثبت نام آزاد سازمانی',
                'price': 200000
            }]

        items = []
        members_pk = set()

        for team in self.teams.all():
            
            items.append({
                'title': team.competition_field.name,
                'price': team.competition_field.price
            })
            
            for member in team.participants.all():
                members_pk.add(member.pk)
        items.append({
            'title': 'ثبت نام فردی ' + str(len(members_pk)) + ' نفر',
            'price': 90000 * len(members_pk)
        })
        print(items)
        return items

    @property
    def payment_done(self):
        for invoice in self.invoices.all():
            if invoice.success:
                return True
        return False

    @property
    def payment_amount(self):
        if not self.teams.exists():
            return None
        team_type = self.teams.first().team_type
        
        if team_type == TeamTypeConsts.PUBLIC_STUDENT:
            return 100000
        elif team_type == TeamTypeConsts.PUBLIC_ORGANIZATION:
            return 200000

        amount = 0
        members_pk = set()

        for team in self.teams.all():
            amount += team.competition_field.price
            for member in team.participants.all():
                members_pk.add(member.pk)

        return amount + 90000 * len(members_pk)

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
    uploaded_file = models.FileField(upload_to=team_uploaded_file_upload_location,null=True, blank=True)
    
    @property
    def uploaded_file_url(self):
        if self.uploaded_file and hasattr(self.uploaded_file, 'url'):
            return self.uploaded_file.url

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.manager.name