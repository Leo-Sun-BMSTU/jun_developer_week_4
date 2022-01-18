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


# def my_company_create(request):
#     """
#
#     :param request:
#     :return:
#     """
#     if request.user.is_anonymous:
#         return redirect('accounts:login')
#     if not Company.objects.get(owner_id=request.user.id):
#         return render(
#             request,
#             'company_create.html',
#             context={
#                 'form': CompanyForm,
#             }
#         ), HttpResponseRedirect('my_company')


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


# def lets_start(request):
#     """
#
#     :param request:
#     :return:
#     """
#     if request.user.is_anonymous:
#         redirect('accounts:login')
#     form = CompanyForm(request.POST, request.FILES)
#     if form.is_valid():
#         company = form.save(commit=False)
#         company.owner = User.objects.get(id=request.user.id)
#         company.save()
#         return redirect('vacancies:my_company')
#     messages.error(request, 'Неверные данные!')
#     return render(
#         request,
#         'company_create.html',
#         context={
#             'form': form,
#         }
#     )


# @login_required
# def my_company_edit(request):
#     """
#
#     :param request:
#     :return:
#     """
#     company = Company.objects.get(owner_id=request.user.id)
#     form = CompanyForm(request.POST, request.FILES)
#     if form.is_valid():
#         company.update(**form.changed_data)
#         return redirect('vacancies:my_company')


class MyCompanyView(views.View):
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
            company = Company.objects.get(owner=request.user)
            if company:
                return render(
                    request,
                    'my_company.html',
                    context={
                        'form': CompanyForm(instance=company)
                    }
                )
            if Company.objects.get(owner=request.user).DoesNotExist:
                return redirect('vacancies:my_company_create')

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


        # if not request.user.is_anonymous:
        #     user = request.user
        #     form = None
        #     try:
        #         user_company = Company.objects.get(owner=user)
        #     except Company.DoesNotExist:
        #         user_company = None
        #     if user_company:
        #         form = CompanyForm(instance=user_company)
        #         return render(
        #             request,
        #             'company.html',
        #             context={
        #                 'form': form,
        #                 'company': user_company,
        #                 'vacancy_count': Vacancy.objects.filter(company_id=user_company.id)
        #             }
        #         )
        #     return redirect('vacancies:my_company_create')

    # def post(self, request):
    #     """
    #
    #     :param request:
    #     :return:
    #     """
    #     if not request.user.is_anonymous:
    #         user = request.user
    #         user_company = Company.objects.get(owner=user)
    #         form = CompanyForm(request.POST, request.FILES, instance=user_company)
    #         if form.is_valid():
    #             messages.info(request, 'Информация обновлена')
    #         else:
    #             messages.error(request, 'Введены неверные данные!')
    #             return render(
    #                 'company.html',
    #                 context={
    #                     'form': form,
    #                 }
    #             )


class MyCompanyCreateView(LoginRequiredMixin, views.View):
    """

    """
    def get(self, request):
        """

        :param request:
        :return:
        """
        company = Company.objects.get(owner=request.user)
        if company:
            return redirect('vacancies:my_company')
        form = CompanyForm()
        return render(
            request,
            'company.html',
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
            messages.info(request, 'Компания была создана')
        else:
            messages.error(request, 'Проверьте правильность введенной информации!')
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


class MyCompanyVacancyCreateView(LoginRequiredMixin, views.View):
    """

    """
    def get(self, request):
        """

        :param request:
        :return:
        """
        return render(
            request,
            ''
        )
