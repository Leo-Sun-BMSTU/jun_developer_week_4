from django import views
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView

from vacancies.forms import ApplicationForm, CompanyForm
from vacancies.models import Specialty, Vacancy, Company, Application
from vacancies.support_functions import count_specialties, count_vacancies_by_company, vacancy_grouping_by_specialty


def index(request):
    """

    :param request:
    :return:
    """
    return render(
        request,
        'index.html',
        context={
            'specialties': Specialty.objects.all(),
            'vacancy_count_by_specialties': dict(count_specialties()),
            'companies': Company.objects.all(),
            'vacancy_count_by_companies': count_vacancies_by_company(),
        })


def for_base(request):
    """

    :param request:
    :return:
    """
    return render(
        request,
        'base.html',
        context={
            'request': request,
        }
    )


def vacancy_by_specialty(request, specialty_code: str):
    """

    :param request:
    :param specialty_code:
    :return:
    """
    specialty = get_object_or_404(Specialty, code=specialty_code)
    specialty_id = Specialty.objects.get(code=specialty_code).id
    return render(
        request,
        'vacancies_by_specialty.html',
        context={
            'vacancies_by_specialties': Vacancy.objects.filter(specialty_id=specialty_id),
            'vacancies_count': Vacancy.objects.filter(specialty_id=specialty_id).count(),
            'specialty_name': specialty.title,
        })


def all_vacancies(request):
    """

    :param request:
    :return:
    """
    return render(
        request,
        'vacancies.html',
        context={
            'vacancies_by_specialties': vacancy_grouping_by_specialty(),
            'vacancies_count': {key: len(value) for key, value in vacancy_grouping_by_specialty().items()},
        })


def company_info(request, company_id: int):
    """

    :param company_id:
    :param request:
    :return:
    """
    company = get_object_or_404(Company, id=company_id)
    return render(
        request,
        'company.html',
        context={
            'company': company,
            'company_vacancies': Vacancy.objects.filter(company_id=company_id),
            'company_vacancies_count': Vacancy.objects.filter(company_id=company_id).count(),
        })


def my_company_create(request):
    """

    :param request:
    :return:
    """
    if request.user.is_anonymous:
        return redirect('accounts:login')
    if not Company.objects.get(owner_id=request.user.id):
        return render(
            request,
            'company_create.html',
            context={
                'form': CompanyForm,
            }
        )


def send_application(request, vacancy_id: int):
    """
    View function informed about success sending of application
    :param request:
    :param vacancy_id:
    :return:
    """
    # if request.user.is_anonymous:
    #     return redirect('accounts:login')
    return render(
        request,
        'send_application.html',
        context={
            'request': request
        })


class VacancyView(views.View):
    """

    """
    form_class = ApplicationForm
    template_name = 'vacancy.html'

    def get(self, request, vacancy_id):
        """

        :param request:
        :param vacancy_id:
        :return:
        """
        vacancy = get_object_or_404(Vacancy, id=vacancy_id)
        company = Company.objects.get(id=vacancy.company_id)
        return render(
            request,
            self.template_name,
            context={
                'vacancy': vacancy,
                'company': company,
                'form': ApplicationForm,
            })

    def post(self, request, vacancy_id: int):
        """

        :param vacancy_id:
        :param request:
        :return:
        """
        form = ApplicationForm(request.POST)
        vacancy = get_object_or_404(Vacancy, id=vacancy_id)
        company = Company.objects.get(id=vacancy.company_id)
        if form.is_valid():
            form.save()
            return redirect('vacancies:send_application')
        messages.error('Неверные данные!')
        return render(
            request,
            self.template_name,
            context={
                'vacancy': vacancy,
                'company': company,
                'form': form,
            }
        )
        # vacancy = get_object_or_404(Vacancy, id=vacancy_id)
        # company = Company.objects.get(id=vacancy.company_id)
        # form = ApplicationForm(request.POST)
        # print(form.cleaned_data)
        # if form.is_valid():
        #     form.save()
        # # Application.objects.create(**form.cleaned_data)
        #     return redirect('vacancies:send_application')
        # messages.error(request, 'Error!')
        # return render(
        #     request,
        #     self.template_name,
        #     context={
        #         'vacancy': vacancy,
        #         'company': company,
        #         'form': form,
        #     })


def my_company_info(request):
    """

    :param request:
    :return:
    """
    company = Company.objects.get(owner_id=request.user.id)
    if request.user.is_anonymous:
        return redirect('accounts:login')
    return render(
        request,
        'company.html',
        context={
            'company': company,
            'company_vacancies': Vacancy.objects.filter(company_id=company.id),
            'company_vacancies_count': Vacancy.objects.filter(company_id=company.id).count(),
        }
    )


class MyCompanyView(views.View):
    """

    """


class MyCompanyVacancies(views.View):
    """

    """
    # def as_view(cls, **initkwargs):
    #     """
    #
    #     :param initkwargs:
    #     :return:
    #     """
    pass


class MyCompanyVacancy(views.View):
    """

    """
    # def as_view(cls, **initkwargs):
    #     pass
    pass


# class UserLoginView(LoginView):
#     """
#
#     """
#     redirect_authenticated_user = True
#     template_name = 'login.html'
#
#
# class UserSignupView(CreateView):
#     form_class = UserCreationForm
#     success_url = 'login'
#     template_name = 'signup.html'
