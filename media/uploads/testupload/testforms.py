from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.

from django.forms import ModelForm
from .models import BookInstance

class RenewBookModelForm(ModelForm):
    class Meta:
        model = BookInstance
        fields = ['due_back', 'status', 'imprint']
        labels = {'due_back': _('Renewal date'),}
        help_texts = {'due_back': _('Enter a date between now and 4 weeks (default 3).'),}
        # required_css_class = 'bold'
        # widgets = {
        #     'due_back': forms.SplitDateTimeWidget
        # }

    # class RenewBookForm(forms.Form):
#     renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean(self):
        # Syntax clean_field_name
        # This method is to perform validation of the field renewal_date
        # It will be called when is_valid() method is called on the form instance
        data = self.cleaned_data['due_back']

        # Check date is not in past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check date is in range librarian allowed to change (+4 weeks).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            # raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))
            self.add_error('due_back', "Invalid date - renewal more than 4 weeks ahead")
            # self.add_error('borrower', "Invalid value ....")
            # raise forms.ValidationError([
            #     forms.ValidationError("Invalid date - renewal more than 4 weeks ahead"),
            #     forms.ValidationError("")
            # ])

        # Remember to always return the cleaned data.
        # return data

    def __init__(self, *args, **kwargs):
        super(RenewBookModelForm, self).__init__(*args, **kwargs)