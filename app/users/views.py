from django.shortcuts import render, redirect
from django.views.generic import View

from users.forms import UserRegistrationForm, UserEditForm, UserDeleteForm


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
        return render(request, 'account/user/detail.html', {'user': user, 'orders': user.orders.all()})


class UserEditView(View):
    def post(self, request, *args, **kwargs):
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
            return redirect('users:user_detail')

        return render(request, 'account/edit.html', {'user_form': user_form})

    def get(self, request):
        user_form = UserEditForm(instance=request.user)

        return render(request, 'account/edit.html', {'user_form': user_form})


class UserDeleteView(View):
    def post(self, request, *args, **kwargs):
        delete_form = UserDeleteForm(user=request.user, data=request.POST)

        if delete_form.is_valid():
            request.user.is_active = False
            request.user.save()
            return redirect('users:logout')

        return render(request, 'account/delete.html', {'delete_form': delete_form})

    def get(self, request):
        delete_form = UserDeleteForm(user=request.user)
        return render(request, 'account/delete.html', {'delete_form': delete_form})
