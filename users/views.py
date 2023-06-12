from django.shortcuts import render
from django.views.generic import View
from django.contrib import messages

from users.forms import UserRegistrationForm, UserEditForm


class RegisterView(View):
    def post(self, request, *args, **kwargs):
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'account/register_done.html', {'new_user': new_user})

        return render(request, 'account/register.html', {'user_form': user_form})

    def get(self, request):
        user_form = UserRegistrationForm()
        return render(request, 'account/register.html', {'user_form': user_form})


class UserView(View):
    def get(self, request):
        user = request.user
        return render(request, 'account/user/detail.html', {'user': user,
                                                            'orders': user.orders.all()})


class UserEditView(View):
    def post(self, request, *args, **kwargs):
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Profile updated successfully!')
        else:
            messages.error(request, 'Error updating your profile')

        return render(request, 'account/edit.html', {'user_form': user_form})

    def get(self, request):
        user_form = UserEditForm(instance=request.user)

        return render(request, 'account/edit.html', {'user_form': user_form})
