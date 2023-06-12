from django import forms

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
