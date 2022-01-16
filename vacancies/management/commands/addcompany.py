from django.core.management.base import BaseCommand

from vacancies.models import Company
from vacancies import data


class Command(BaseCommand):
    help = 'Add new vacancy to database'

    def handle(self, *args, **options):
        '''

        :param args:
        :param options:
        :return:
        '''
        for company in data.companies:
            company_instance = Company.objects.create(id=company.get('id'),
                                                      name=company.get('title'),
                                                      location=company.get('location'),
                                                      logo=company.get('logo'),
                                                      description=company.get('description'),
                                                      employee_count=company.get('employee_count'))
