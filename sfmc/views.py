from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from competition.models import CompetitionField, Participant, Team, TeamTypeConsts, Adviser


def dashboard_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('register'))
    the_profile = request.user.profile
    teams = the_profile.teams.all()
    if teams[0].team_type == TeamTypeConsts.PARTICIPANT:
        if request.method == 'POST':
            the_team = Team.objects.get(pk = int(request.POST['team_pk']))
            the_team.upload_date = timezone.now()
            the_team.uploaded_file = request.FILES['team_uploaded_file']
            the_team.save()
        return render(request, 'dashboard_team.html',
                      {'teams': teams})
    return render(request, 'dashboard_public.html',
                  {'team': teams[0]})


def register_view(request):
    template = 'register.html'
    if request.user.is_authenticated and not request.user.is_superuser:
        return HttpResponseRedirect(reverse('dashboard'))

    valid_team_types = [{'title': team_type[1], 'value': team_type[0]} for team_type in TeamTypeConsts.states]

    if request.method == 'POST':
        with transaction.atomic():
            print(request.POST)
            print(request.FILES)

            the_user = User.objects.create_user(
                username=request.POST['manager_email'].strip(),
                password=request.POST['manager_password_1'],
            )

            the_manager = Participant.objects.create(
                user=the_user,
                name=request.POST['manager_name'].strip(),
                phone_number=request.POST['manager_phone_number'].strip(),
                email=request.POST['manager_email'].strip(),
            )

            if request.POST['team_type'] == TeamTypeConsts.PARTICIPANT:

                the_manager.university = request.POST['manager_university'].strip()
                the_manager.student_card_image = request.FILES['manager_student_card_image']
                the_manager.save()

                members = {}
                if request.POST['active_members']:
                    for active_member in request.POST['active_members'].split(','):
                        members[active_member] = Participant.objects.create(
                            name=request.POST['member_' + active_member + '_name'].strip(),
                            phone_number=request.POST['member_' + active_member + '_phone_number'].strip(),
                            email=request.POST['member_' + active_member + '_email'].strip(),
                            university=request.POST['member_' + active_member + '_university'].strip(),
                            student_card_image=request.FILES['member_' + active_member + '_student_card_image']
                        )

                for competition_field in CompetitionField.objects.all():
                    if 'competition_' + str(competition_field.pk) in request.POST:
                        the_team = Team.objects.create(
                            name=request.POST['competition_' + str(competition_field.pk) + '_team_name'],
                            manager=the_manager,
                            team_type=request.POST['team_type'],
                            competition_field=competition_field
                        )

                        the_team.participants.add(the_manager)

                        if competition_field.needs_adviser:
                            the_adviser = Adviser.objects.create(
                                name=request.POST['competition_' + str(competition_field.pk) + '_adviser_name'],
                                email=request.POST['competition_' + str(competition_field.pk) + '_adviser_email'],
                                university=request.POST[
                                    'competition_' + str(competition_field.pk) + '_adviser_university'],
                            )
                            the_team.adviser = the_adviser
                            the_team.save()

                        for active_member in request.POST['active_members'].split(','):
                            if 'member_' + active_member + '_competition_' + str(
                                    competition_field.pk) in request.POST:
                                the_team.participants.add(members[active_member])

            else:

                the_team = Team.objects.create(
                    manager=the_manager,
                    team_type=request.POST['team_type']
                )

                the_team.participants.add(the_manager)

                if request.POST['team_type'] == TeamTypeConsts.PUBLIC_STUDENT:
                    the_manager.university = request.POST['manager_university'].strip()
                    the_manager.student_card_image = request.FILES['manager_student_card_image']
                else:
                    the_manager.organization = request.POST['manager_organization'].strip()
                    the_manager.student_card_image = request.FILES['manager_national_card_image']

                the_manager.save()

            login(request, the_user)
        return HttpResponseRedirect(reverse('dashboard'))
    return render(request, template,
                  {'competition_fields': CompetitionField.objects.all(), 'valid_team_types': valid_team_types})


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('dashboard'))

    err = False
    if request.method == 'POST':
        try:
            u = User.objects.get(username = request.POST['username'].strip())
        except:
            err = True
        else:
            if u.check_password(request.POST['password']):
                login(request, u)
                return HttpResponseRedirect(reverse('dashboard'))
            else:
                err = True
    return render(request, "login.html", {'err': err})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

def index_view(request):
    return render(request, "index.html", {})


def about_view(request):
    return render(request, "about.html", {})


def regulations_view(request):
    return render(request, "regulations.html", {})


def clipart_view(request):
    return render(request, "clipart.html", {})


def project_view(request):
    return render(request, "project.html", {})


def idea_show_view(request):
    return render(request, "idea_show.html", {})


def virtual_lab_view(request):
    return render(request, "virtual_lab.html", {})


def history_view(request):
    return render(request, "history.html", {})


def calendar_view(request):
    return render(request, "calendar.html", {})


def hovercraft_view(request):
    return render(request, "hovercraft.html", {})


def poster_view(request):
    return render(request, "poster.html", {})


def contactus_view(request):
    return render(request, "contactus.html", {})


def prizes_view(request):
    return render(request, "prizes.html", {})
