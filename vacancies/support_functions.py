from collections import Counter

from django.db.models import Count

from vacancies.models import Vacancy, Specialty, Company


def count_specialties() -> dict:
    """

    :return:
    """
    specialty_ids_list = list(Vacancy.objects.values_list('specialty_id', flat=True))
    specialty_code_list = [Specialty.objects.get(id=specialty).code for specialty in specialty_ids_list]
    specialties_count = Counter(specialty_code_list)
    return specialties_count


def count_vacancies_by_company() -> dict:
    """

    :return:
    """
    company_ids_list = list(Vacancy.objects.values_list('company_id', flat=True))
    company_names_list = [Company.objects.get(id=company_id).name for company_id in company_ids_list]
    company_count = Counter(company_names_list)
    return dict(company_count)


def vacancy_grouping_by_specialty() -> dict:
    """

    :return:
    """
    result = {}
    for specialty in Specialty.objects.all():
        result[specialty.code] = Vacancy.objects.filter(specialty_id=specialty.id)
    return result
