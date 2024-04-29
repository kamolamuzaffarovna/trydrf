from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.urls import reverse_lazy
from .models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("PASSWORDS DO NOT MATCH")
            return password2
        raise forms.ValidationError("YOU SHOULD WRITE PASSWORDS")

    def save(self, commit=True):
        account = super().save(commit=False)
        account.set_password(self.cleaned_data["password1"])
        if commit:
            account.save()
        return account


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'avatar', 'is_active', 'is_staff', 'is_superuser')

        def __init__(self, *args, **kwargs):
            super(UserChangeForm, self).__init__(*args, **kwargs)
            self.fields['password'].help_text = '<a href="%s">change password</a>' % reverse_lazy(
                'admin:auth_user_password_change', args=[self.instance.id])

        def clean_password(self):
            return self.initial['password']