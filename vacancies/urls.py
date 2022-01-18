from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from vacancies import views


app_name = 'vacancies'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    path('vacancies/cat/<slug:specialty_code>', views.vacancy_by_specialty, name='vacancy_by_specialty'),
    path('vacancies/', views.all_vacancies, name='all_vacancies'),
    path('vacancies/<int:vacancy_id>', views.VacancyView.as_view(), name='vacancy_info'),
    path('vacancies/<int:vacancy_id>/send', views.send_application, name='send_application'),

    path('companies/<int:company_id>', views.company_info, name='company_info'),

    path('mycompany/', views.MyCompanyView.as_view(), name='my_company'),
    path('mycompany/create', views.MyCompanyCreateView.as_view(), name='my_company_create'),
    path('mycompany/vacancies', views.MyCompanyVacancies.as_view(), name='my_company_vacancies'),
    path('mycompany/vacancies/<int:vacancy_id>', views.MyCompanyVacancy.as_view(), name='my_company_vacancy'),
    path('mycompany/vacancies/create', views.MyCompanyCreateVacancy.as_view(), name='my_vacancy_create'),
    path('mycompany/letsstart', views.MyCompanyView.as_view(), name='my_company_lets_start')
]

# urlpatterns += [
#     path('login', UserLoginView.as_view(), name='login'),
#     path('logout', LogoutView.as_view(), name='logout'),
#     path('signup', UserSignupView.as_view(), name='signup'),
# ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
