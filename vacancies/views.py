import os.path

from django import views
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, reverse

from django.views.generic import CreateView

from vacancies.forms import ApplicationForm, CompanyForm, VacancyForm
from vacancies.models import Specialty, Vacancy, Company, Application
from vacancies.support_functions import count_specialties, count_vacancies_by_company, vacancy_grouping_by_specialty


class IndexView(views.View):
    """
    Класс представления главной страницы.
    Class based view of main page.
    """
    def get(self, request):
        """
        Функция отображения основной информации на главной страницу.
        GET function of main information.
        :param request:
        :return:
        """
        return render(
            request,
            'index.html',
            context={
                'companies': Company.objects.all().prefetch_related('vacancies'),
                'specialties': Specialty.objects.all(),
            }
        )


def for_base(request):
    """
    Функция настройки базового шаблона, передаёт в него полученный запрос.
    Customization function for base template, it transmits received request.
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
    Функция представления отображает группу вакансий определённого направления согласно переданному коду в адресе запроса.
    View function get vacancies group of certain direction according with code in url request.
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
    Функция представления отображает все созданные вакансии.
    GET function of all created vacancies.
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
    Функция представления отображает информацию о компании с номером, переданным в адресе запроса.
    GET function informed about company with id from url request.
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


def send_application(request, vacancy_id: int):
    """
    Функция представления отображает страницу с сообщением об успешной отправке отклика на вакансию.
    View function informed about success sending of application.
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
    Класс представления вакансии.
    Class based view for vacancy.
    """
    form_class = ApplicationForm
    template_name = 'vacancy.html'

    def get(self, request, vacancy_id):
        """
        Функция отображения вакансии предоставляет информацию о конкретной вакансии и предоставляет доступ
        к форме для отправки отклика.
        GET function for vacancy information and access to application form.
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
        Функция отправки формы отклика на вакансию.
        POST function send application form.
        :param vacancy_id:
        :param request:
        :return:
        """
        form = ApplicationForm(request.POST)
        vacancy = get_object_or_404(Vacancy, id=vacancy_id)
        company = Company.objects.get(id=vacancy.company_id)
        if form.is_valid():
            application = form.save(commit=False)
            application.vacancy = Vacancy.objects.get(id=vacancy_id)
            application.user = User.objects.get(id=request.user.id)
            application.save()
            return redirect('vacancies:send_application', vacancy_id)
        messages.error(request, 'Неверные данные!')
        return render(
            request,
            self.template_name,
            context={
                'vacancy': vacancy,
                'company': company,
                'form': form,
            }
        )


class MyCompanyView(LoginRequiredMixin, views.View):
    """

    """
    def get(self, request):
        """

        :param request:
        :return:
        """
        if request.user.is_anonymous:
            return redirect('accounts:login')
        else:
            try:
                company = Company.objects.get(owner=request.user)
                return render(
                    request,
                    'my_company.html',
                    context={
                        'form': CompanyForm(instance=company),
                        'company': company,
                    }
                )
            except Company.DoesNotExist:
                return redirect('vacancies:my_company_create')
            # company = Company.objects.get(owner=request.user)

    def post(self, request):
        """

        :param request:
        :return:
        """
        company = Company.objects.get(owner=request.user)
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            messages.info(request, 'Информация обновлена')
        else:
            messages.error(request, 'Неверные данные')
            return render(
                request,
                'my_company.html',
                context={
                    'form': form,
                }
            )


class MyCompanyCreateView(LoginRequiredMixin, views.View):
    """

    """
    def get(self, request):
        """

        :param request:
        :return:
        """
        try:
            company = Company.objects.get(owner=request.user)
            return redirect('vacancies:my_company')
        except Company.DoesNotExist:
            form = CompanyForm()
            return render(
                request,
                'my_company.html',
                context={
                    'form': form,
                }
            )

    def post(self, request):
        """

        :param request:
        :return:
        """
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            user_company_instance = form.save(commit=False)
            user_company_instance.owner = request.user
            user_company_instance.save()
            messages.info(request, 'Компания создана')
        else:
            messages.error(request, 'Неверные данные')
            return render(
                request,
                'company.html',
                context={
                    'form': form
                })
        return redirect('vacancies:my_company')


def my_company_info(request):
    """

    :param request:
    :return:
    """
    if request.user.is_anonymous:
        return redirect('accounts:login')
    try:
        company = Company.objects.get(owner_id=request.user.id)
        return render(
            request,
            'company.html',
            context={
                'company': company,
                'company_vacancies': Vacancy.objects.filter(company_id=company.id),
                'company_vacancies_count': Vacancy.objects.filter(company_id=company.id).count(),
            }
        )
    except Company.DoesNotExist:
        return redirect('vacancies:my_company_lets_start')


class MyCompanyVacancies(views.View):
    """

    """
    def get(self, request):
        """

        :param request:
        :return:
        """
        if request.user.is_anonymous:
            return redirect('accounts:login')
        else:
            try:
                vacancies = Vacancy.objects.filter(company__owner=request.user).all()
                return render(
                    request,
                    'my_company_vacancies.html',
                    context={
                        'vacancies': vacancies,
                    }
                )
            except Vacancy.DoesNotExist:
                messages.info(request, 'Нет вакансий')
                return redirect('vacancies:my_vacancy_create')


class MyCompanyCreateVacancy(LoginRequiredMixin, views.View):
    """

    """
    def get(self, request):
        """

        :param request:
        :return:
        """
        form = VacancyForm()
        return render(
            request,
            'my_company_vacancy_edit.html',
            context={
                'form': form,
            }
        )

    def post(self, request):
        """

        :param request:
        :return:
        """
        form = VacancyForm(request.POST)
        if form.is_valid():
            vacancy_form = form.save(commit=False)
            vacancy_form.company = Company.objects.get(owner=request.user)
            vacancy_form.save()
            messages.info(request, 'Вакансия успешно создана')
        else:
            messages.error(request, 'Неверные данные')
            return render(
                request,
                'my_company_vacancy_edit.html',
                context={
                    'form': form,
                }
            )
        return redirect('vacancies:my_company_vacancies')


class MyCompanyVacancy(LoginRequiredMixin, views.View):
    """

    """
    def get(self, request, vacancy_id: int):
        """

        :param vacancy_id:
        :param request:
        :return:
        """
        try:
            vacancy = Vacancy.objects.get(id=vacancy_id)
            return render(
                request,
                'my_company_vacancy_edit.html',
                context={
                    'vacancy_id': vacancy_id,
                    'vacancy': vacancy,
                    'form': VacancyForm(instance=vacancy),
                }
            )
        except Vacancy.DoesNotExist:
            messages.error(request, 'Такой вакансии нет')
            return redirect('vacancies:my_company_vacancies')

    def post(self, request, vacancy_id: int):
        """

        :param request:
        :param vacancy_id:
        :return:
        """
        vacancy = Vacancy.objects.get(id=vacancy_id)
        form = VacancyForm(request.POST, instance=vacancy)
        if form.is_valid():
            form.save()
            messages.info(request, 'Информация обновлена')
        else:
            messages.error(request, 'Неверные данные')
            return render(
                request,
                'my_company_vacancy_edit.html',
                context={
                    'form': form,
                    'vacancy_id': vacancy_id,
                }
            )
