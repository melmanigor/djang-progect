from django import forms
from vacation.models import Vacation, Country
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit , Layout, Fieldset, ButtonHolder, Button
from datetime import date

class VacationForm(forms.Form):
    
    """
    Form for selecting a country to filter vacations.
    """
    country = forms.ModelChoiceField(queryset=Country.objects.all(),label='Select Country',required=True)
class VacationCreateForm(forms.ModelForm):

    """
    Form for creating a new vacation, excluding 'liked_by'.
    Includes crispy layout and date validation.
    """
    class Meta:
        model = Vacation
   
        exclude = ['liked_by']

        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }   
    def __init__(self, *args, **kwargs)->None:
        """
    Initialize the form with Crispy Forms layout.

    - Sets the form method to POST.
    - Disables default <form> tag rendering.
    - Applies a structured layout with a fieldset and action buttons.
    - Adds a 'Cancel' button that redirects to the vacation list page.
    """
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
    def clean(self)->dict:
        """
        Validate date logic:
        - start_date must be in the future
        - end_date must be after start_date and not in the past
        """
        
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

        return cleaned_data

class VacationUpdateForm(forms.ModelForm):
    """
    Form for updating an existing vacation.
    Includes crispy layout and ensures valid date range.
    """
    class Meta:
        model = Vacation
        exclude = ['liked_by']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def  __init__(self, *args, **kwargs)->None:
        """
    Initialize the VacationUpdateForm with custom Crispy Forms layout.

    - Sets the 'image' field as optional (not required).
    - Configures Crispy Forms helper to:
        - Use POST method.
        - Not render <form> tag automatically (useful in custom templates).
        - Display a clean layout with:
            - Fieldset titled 'Update Vacation'.
            - Fields: country, description, start_date, end_date, image, price.
            - Action buttons: 'Save' (submit) and 'Cancel' (redirects to vacation list).
        """
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
    def clean(self)->dict:
        """
        Ensure end date is after start date.
        """
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date > end_date:
            self.add_error('end_date', 'End date must be after start date.')

        return cleaned_data

