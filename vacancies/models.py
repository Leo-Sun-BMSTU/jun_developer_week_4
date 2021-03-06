from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings


class Company(models.Model):
    """
    Класс для модели компании.
    Company model class.
    """
    name = models.CharField(max_length=64)
    location = models.CharField(max_length=64)
    employee_count = models.IntegerField()
    logo = models.ImageField(upload_to=settings.MEDIA_COMPANY_IMAGE_DIR, default='')
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="companies")


class Specialty(models.Model):
    """
    Класс для модели специальности.
    Specialty model class.
    """
    code = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    picture = models.ImageField(upload_to=settings.MEDIA_SPECIALITY_IMAGE_DIR)


class Vacancy(models.Model):
    """
    Класс для модели вакансии.
    Vacancy model class.
    """
    title = models.CharField(max_length=64)
    specialty = models.ForeignKey(Specialty, related_name='vacancies',
                                  on_delete=models.CASCADE, null=True)
    company = models.ForeignKey(Company, related_name='vacancies',
                                on_delete=models.CASCADE, null=True)
    skills = models.CharField(max_length=64)
    description = models.TextField()
    salary_min = models.FloatField()
    salary_max = models.FloatField()
    published_at = models.DateField()


class Application(models.Model):
    """
    Класс для модели отклика.
    Application model class.
    """
    written_username = models.CharField(max_length=64)
    written_phone = PhoneNumberField()
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy, related_name='applications', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='applications', on_delete=models.CASCADE)
