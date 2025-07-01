from django.core import validators

from django import forms
from .models import User, UserAddress
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirm', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('phone', 'password', 'is_active', 'is_admin')


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Enter your Phone Or Email Address'}
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Password'}
        ))

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if len(phone) > 40:
            raise ValidationError("invalid value: %(value)s" % {'value': phone}, code='invalid')
        return phone


class RegisterForm(forms.Form):
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Phone Number'}
        ),
        validators=[validators.MinLengthValidator(11)]
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'password'}
        )
    )

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8 :
            raise ValidationError("Password must be at least 8 characters")
        return password

class CheckOtpForm(forms.Form):
    code = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Otp Number'}
        ),
        validators=[validators.MinLengthValidator(5)]
    )


class AddAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})