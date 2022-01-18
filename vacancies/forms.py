from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from phonenumber_field.formfields import PhoneNumberField

from vacancies.models import Application, Company, Vacancy


class ApplicationForm(forms.ModelForm):
    """
    Класс формы отклика на вакансию.
    Form class for application to a vacancy.
    """
    class Meta:
        """
        Класс настройки и создания формы отклика из модели отклика.
        Creating and customization application form from application model.
        """
        model = Application
        fields = ('written_username', 'written_phone', 'written_cover_letter')
        labels = {
            'written_username': 'Ваше имя',
            'written_phone': 'Номер телефона',
            'written_cover_letter': 'Сопроводительное письмо',
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Откликнуться'))


class CompanyForm(forms.ModelForm):
    """
    Класс формы компании.
    Form class for company.
    """
    class Meta:
        """
        Класс настройки и создания формы компании из модели компании.
        Creating and customization company form from company model.
        """
        model = Company
        fields = ('name', 'location', 'employee_count', 'logo', 'description')
        labels = {
            'name': 'Название компании',
            'location': 'Расположение',
            'employee_count': 'Количество сотрудников',
            'logo': 'Логотип',
            'description': 'Описание',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Создать'))


class VacancyForm(forms.ModelForm):
    """
    Класс формы вакансии.
    Form class for vacancy.
    """
    class Meta:
        """
        Класс настройки и создания формы компании из модели вакансии.
        Creating and customization company form from vacancy model.
        """
        model = Vacancy
        fields = ('title', 'skills', 'description', 'salary_min', 'salary_max', 'published_at')
        labels = {
            'title': 'Название вакансии',
            'skills': 'Навыки',
            'description': 'Описание',
            'salary_min': 'Минимальная ставка',
            'salary_max': 'Максимальная ставка',
            'published_at': 'Дата публикации',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Создать'))
