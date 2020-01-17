from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth import login, logout

from competition.models import CompetitionField, Participant, Team, TeamTypeConsts, Adviser
from django.urls import reverse


# Create your views here.
# testing git

def hello(request):
    return HttpResponse("hello")


def home_view(request):
    template = 'competition/home.html'
    error_message = ""
    if request.user.is_authenticated:
        competition_fields = CompetitionField.objects.all()
        manager = Manager.objects.get(user=request.user)
        participants = Participant.objects.filter(manager=manager)
        teams = Team.objects.filter()
        return render(request, template, {'error_message': error_message, 'competition_fields': competition_fields, })
    else:
        return HttpResponseRedirect(reverse('competition:registeration'))


def registeration_view(request):
    template = 'register.html'
    if request.user.is_authenticated and not request.user.is_superuser:
        return HttpResponseRedirect(reverse('competition:home'))
    else:
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
                                    university=request.POST['competition_' + str(competition_field.pk) + '_adviser_university'],
                                )
                                the_team.adviser = the_adviser
                                the_team.save()

                            for active_member in request.POST['active_members'].split(','):
                                if 'member_' + active_member + '_competition_' + str(competition_field.pk) in request.POST:
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
            # form = RegisterationForm(request.POST)
            # if form.is_valid():
            #     if User.objects.filter(username=form.cleaned_data['email']).exists():
            #         return render(request, template, {
            #             'form': form,
            #             'error_message': 'شما قبلا ثبت نام کرده اید'
            #         })
            #     else:
            #         # Create the user:
            #         # Create participant
            #         user = User.objects.create_user(
            #             username=form.cleaned_data['email'],
            #             password=form.cleaned_data['password'],
            #         )
            #         user.save()
            #         manager = Manager(
            #             user=user,
            #             first_name=form.cleaned_data['first_name'],
            #             last_name=form.cleaned_data['last_name'],
            #             phone_number=form.cleaned_data['phone_number'],
            #             email=form.cleaned_data['email'],
            #             student_card_image=form.cleaned_data['student_card_image'],
            #             university=form.cleaned_data['university']
            #         )
            #         manager.save()
            #         participant = Participant(
            #             manager=manager,
            #             first_name=form.cleaned_data['first_name'],
            #             last_name=form.cleaned_data['last_name'],
            #             phone_number=form.cleaned_data['phone_number'],
            #             email=form.cleaned_data['email'],
            #             student_card_image=form.cleaned_data['student_card_image'],
            #             university=form.cleaned_data['university']
            #         )
            #         participant.save()
            #         login(request, user)
            #         return HttpResponseRedirect(reverse('competition:home'))
        # else:
        #     form = RegisterationForm()

        # valid_entry = [entry_year_show(x) for x in range(14)]
        return render(request, template,
                      {'competition_fields': CompetitionField.objects.all(), 'valid_team_types': valid_team_types})

# def login_view(request):
#     template = 'competition/login.html'
#     if request.user.is_authenticated:
#         return HttpResponseRedirect(reverse('competition:home'))
#     else:
#         form = LoginForm(request.POST)
#         if request.method == 'POST':
#             if form.is_valid():
#                 if User.objects.filter(username=form.cleaned_data['username']).exists():
#                     user = User.objects.get(username=form.cleaned_data['username'])
#                     if user.check_password(form.cleaned_data['password']):
#                         login(request, user)
#                         return HttpResponseRedirect(reverse('competition:home'))

#                 return render(request, template, {
#                     'form': form,
#                     'error_message': 'اطلاعات ورودی شما صحیح نمی باشد'
#                 })
#         else:
#             form = LoginForm()
#         return render(request, template, {'form': form})
