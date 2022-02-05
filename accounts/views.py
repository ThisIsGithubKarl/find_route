from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from accounts.forms import UserLoginForm, UserRegistrationForm


__all__ = (
    'login_view',
    'logout_view',
    'registration_view',
)


def login_view(request):
    form = UserLoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        next_page = request.GET.get('next') or '/'

        login(request, user)

        return redirect(next_page)

    context = {'form': form}
    return render(request, 'accounts/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')


# def registration_view(request):
#     form = UserRegistrationForm(request.POST or None)
#     context = {'form': form}
#
#     if request.method == 'POST':
#         if form.is_valid():
#             new_user = form.save(commit=False)
#             new_user.set_password(form.cleaned_data.get('password'))
#             new_user.save()
#
#             context = {'new_user': new_user}
#             return render(request, 'accounts/register_success.html', context)
#         else:
#             return render(request, 'accounts/register.html', context)
#     else:
#         return render(request, 'accounts/register.html', context)


def registration_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data.get('password'))
            new_user.save()

            return render(request, 'accounts/register_success.html', {'new_user': new_user})
        else:
            return render(request, 'accounts/register.html', {'form': form})
    else:
        form = UserRegistrationForm()
        return render(request, 'accounts/register.html', {'form': form})
