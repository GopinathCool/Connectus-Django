from models import Document


from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm



class RegistrationForm(forms.Form):
    username = forms.EmailField(widget=forms.EmailInput({
        'class': 'form-control',
        'placeholder': 'Email'})
    )
    password1 = forms.CharField(widget=forms.PasswordInput({
        'class': 'form-control',
        'placeholder': 'Password'})
    )
    password2 = forms.CharField(widget=forms.PasswordInput({
        'class': 'form-control',
        'placeholder': 'Re-type password'})
    )

    def clean(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise ValidationError('password 1 and password 2 not matched')


class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput({
        'class': 'form-control',
        'placeholder': 'Email'})
    )
    password = forms.CharField(widget=forms.PasswordInput({
        'class': 'form-control',
        'placeholder': 'Password'})
    )


# class UploadFileForm(forms.Form):
#     title = forms.CharField(max_length=50)
#     file = forms.FileField()

class UploadFileForm(ModelForm):
    class Meta:
        model = Document
        fields = '__all__'