from django import forms
from vacation.models import Vacation, Country
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit , Layout, Fieldset, ButtonHolder, Button

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
                Button('cancel', 'Cancel', css_class='btn btn-secondary', onclick="window.location.href='/clothing/'")
            )
        )