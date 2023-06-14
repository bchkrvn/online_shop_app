from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField, PasswordChangeForm, SetPasswordForm
from django.utils.translation import gettext_lazy as _

from users.models import User


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'birth_date']
        labels = {
            "first_name": "Имя",
            "last_name": "Фамилия",
            "email": "Электронная почта",
            "birth_date": "Дата рождения",
            'username': 'Имя пользователя',
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords don't match.")
        return cd['password2']

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use.')
        return data

    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
            raise forms.ValidationError('Username already in use.')
        return data

    # def clean_birth_date(self):
    #     data = self.cleaned_data['birth_date']
    #     if data < datetime.datetime.now().day:
    #         raise forms.ValidationError("Birth date can't be in future")
    #     return data


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'birth_date', ]
        labels = {
            "first_name": "Имя",
            "last_name": "Фамилия",
            "email": "Электронная почта",
            "birth_date": "Дата рождения (год-месяц-день)",
            'username': 'Имя пользователя',
        }

    def clean_email(self):
        data = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id) \
            .filter(email=data)
        if qs.exists():
            raise forms.ValidationError('Email already in use.')
        return data

    def clean_username(self):
        data = self.cleaned_data['username']
        qs = User.objects.exclude(id=self.instance.id) \
            .filter(username=data)
        if qs.exists():
            raise forms.ValidationError('Username already in use.')
        return data


class UserFormAdmin(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput,
                               help_text="Your password can't be too similar")
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput,
                                help_text="Enter the same password as before, for verification")

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords don't match.")
        return cd['password2']

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name',
                  'password', 'password2', 'groups', 'user_permissions',
                  'is_staff', 'is_active']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save(commit=commit)
        return user


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(label=_("Имя пользователя или почта"), widget=forms.TextInput(attrs={"autofocus": True}))
    password = forms.CharField(
        label=_("Пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    error_messages = {
        "invalid_login": _(
            "Пожалуйста, введите корректную почту или имя пользователя и пароль."
        ),
        "inactive": _("Этот аккаунт не активен"),
    }


class CustomPasswordChangeForm(PasswordChangeForm):
    error_messages = {
        "password_mismatch": _("Новые пароли не совпадают между собой"),
        "password_incorrect": _(
            "Ваш старый пароль введен некорректно, пожалуйста, попробуйте еще раз."
        ),
    }
    old_password = forms.CharField(
        label=_("Старый пароль"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True}
        ),
    )
    new_password1 = forms.CharField(
        label=_("Новый пароль"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label=_("Повторите новый пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("Новый пароль"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label=_("Повторите новый пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
