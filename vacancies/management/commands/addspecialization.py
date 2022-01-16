from django.core.management import BaseCommand

from vacancies.models import Specialty
from vacancies import data


class Command(BaseCommand):
    help = 'Add specialty to database'

    def handle(self, *args, **options):
        '''

        :param args:
        :param options:
        :return:
        '''
        for specialty in data.specialties:
            specialty_instance = Specialty.objects.create(code=specialty.get('code'),
                                                          title=specialty.get('title'))
