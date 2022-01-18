from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from phonenumber_field.formfields import PhoneNumberField

from vacancies.models import Application, Company, Vacancy


class ApplicationForm(forms.ModelForm):
    """

    """
    # name = forms.CharField(max_length=60, label='Ваше имя')
    # phone = PhoneNumberField(label='Номер телефона')
    # message = forms.CharField(widget=forms.Textarea, label='Сопроводительное письмо')
    class Meta:
        """

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

    """
    class Meta:
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

    """
    class Meta:
        model = Vacancy
        fields = ('title', 'skills', 'description', 'salary_min', 'salary_max', 'published_at')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Создать'))
