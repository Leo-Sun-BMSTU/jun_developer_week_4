from django.core.management.base import BaseCommand

from vacancies.models import Vacancy, Specialty, Company
from vacancies import data


class Command(BaseCommand):
    help = 'Add new vacancy to database'

    def handle(self, *args, **options):
        '''

        :param args:
        :param options:
        :return:
        '''
        for vacancy in data.jobs:
            vacancy_instance = Vacancy.objects.create(title=vacancy.get('title'),
                                                      specialty=Specialty.objects.get(code=vacancy.get('specialty')),
                                                      company=Company.objects.get(id=vacancy.get('company')),
                                                      skills=vacancy.get('skills'),
                                                      description=vacancy.get('description'),
                                                      salary_min=vacancy.get('salary_from'),
                                                      salary_max=vacancy.get('salary_to'),
                                                      published_at=vacancy.get('posted'))

        # print(Company.objects.all())
