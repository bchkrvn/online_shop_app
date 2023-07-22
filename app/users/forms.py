import datetime

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField, PasswordChangeForm, SetPasswordForm
from django.utils.translation import gettext_lazy as _

from users.models import User


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'birth_date', ]

    def clean_email(self):
        data = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id) \
            .filter(email=data)
        if qs.exists():
            raise forms.ValidationError(_('Этот адрес электронной почты уже используется'))
        return data

    def clean_username(self):
        data = self.cleaned_data['username']
        qs = User.objects.exclude(id=self.instance.id) \
            .filter(username=data)
        if qs.exists():
            raise forms.ValidationError(_('Имя пользователя занято'))
        return data

    def clean_birth_date(self):
        data = self.cleaned_data['birth_date']
        if data > datetime.date.today():
            raise forms.ValidationError(_("Ваш день рождения не может быть в будущем"))
        return data


class UserRegistrationForm(UserEditForm):
    password = forms.CharField(label=_('Пароль'),
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Повторите пароль'),
                                widget=forms.PasswordInput)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError(_("Пароли не совпадают"))
        return cd['password2']


class UserFormAdmin(forms.ModelForm):
    password = forms.CharField(label=_('Пароль'),
                               widget=forms.PasswordInput,
                               help_text=_("Ваш пароль не может быть слишком простым"))
    password2 = forms.CharField(label=_('Повторите пароль'),
                                widget=forms.PasswordInput,
                                help_text=_("Введите тот же пароль, что и до этого"))

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError(_("Пароли не совпадают"))
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
        "invalid_login": _("Пожалуйста, введите корректную почту или имя пользователя и пароль."),
        "inactive": _("Этот аккаунт не активен"),
    }


class CustomPasswordChangeForm(PasswordChangeForm):
    error_messages = {
        "password_mismatch": _("Новые пароли не совпадают между собой"),
        "password_incorrect": _("Ваш старый пароль введен некорректно, пожалуйста, попробуйте еще раз."),
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


class UserDeleteForm(forms.Form):

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    password = forms.CharField(
        label=_("Пароль"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True}
        ),
    )

    def clean_password(self):
        password = self.cleaned_data["password"]
        if not self.user.check_password(password):
            raise forms.ValidationError(_("Неверный пароль"))
        return password
