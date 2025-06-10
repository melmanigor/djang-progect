from django import forms
from vacation.models import Vacation, Country
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit , Layout, Fieldset, ButtonHolder, Button
from datetime import date

class VacationForm(forms.Form):
    country = forms.ModelChoiceField(queryset=Country.objects.all(),label='Select Country',required=True)
class VacationCreateForm(forms.ModelForm):
    class Meta:
        model = Vacation
        
        exclude = ['liked_by']

       
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

          
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = False  
        self.helper.layout = Layout(
            Fieldset(
                'Vacations List',
                'country',
                'description',
                'start_date',
                'end_date',
                'image',
                'price'
             
            ),
            ButtonHolder(
                Submit('submit', 'Save', css_class='btn btn-success'),
                Button('cancel', 'Cancel', css_class='btn btn-secondary', onclick="window.location.href='/vacation/'")
            )
        )
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        today = date.today()
        if start_date and start_date <= today:
            self.add_error('start_date', 'Start date must be in the future.')
        
        if end_date and end_date <= today:
            self.add_error('end_date', 'End date should not be in the past.')
        
        if start_date and end_date and start_date > end_date:
            self.add_error('end_date', 'End date must be after start date.')

class VacationUpdateForm(forms.ModelForm):
    class Meta:
        model = Vacation
        exclude = ['liked_by']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def  __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = False  
        self.helper.layout = Layout(
            Fieldset(
                'Update Vacation',
                'country',
                'description',
                'start_date',
                'end_date',
                'image',
                'price'
            ),
            ButtonHolder(
                Submit('submit', 'Save', css_class='btn btn-success'),
                Button('cancel', 'Cancel', css_class='btn btn-secondary', onclick="window.location.href='/vacation/'")
            )
        )
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date > end_date:
            self.add_error('end_date', 'End date must be after start date.')

