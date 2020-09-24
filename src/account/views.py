from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import *
from .models import Profile
from .ajax import *


def user_login(request):
    """ User login view """
    if request.user.is_authenticated:
        return redirect('account:edit')
        
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('blog:post_list')
                else:
                    return HttpResponse('Ваш аккаунт был отключен. <a '
                                        'href="mailto:r.tsura@zestleaders.com?subject=Отключенный аккаунт"> Свяжитесь '
                                        'с нами</a> для уточнения подробностей.')
            else:
                messages.error(request, 'Указаны неверные данные для входа')
                form = UserLoginForm()
    else:
        form = UserLoginForm()
    
    context = {
        'form': form
    }
    return render(request, 'account/login.html', context)


def user_register(request):
    """ User registration view """
    if request.user.is_authenticated:
        return redirect('account:edit')

    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.email = user_form.cleaned_data['email'].lower()
            new_user.username = new_user.email
            new_user.first_name = user_form.cleaned_data['first_name'].capitalize()
            new_user.last_name = user_form.cleaned_data['last_name'].capitalize()
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()

            Profile.objects.create(user=new_user)

            cd = user_form.cleaned_data
            user_to_login = authenticate(request, username=cd['email'], password=cd['password'])
            login(request, user_to_login)

            messages.success(request, 'Успешная регистрация')
            return redirect('account:edit')
        else:
            messages.error(request, 'Ошибка обновления профиля')

            user_form = UserRegistrationForm()
            return render(request, 'account/register.html', {'user_form': user_form})
    else: 
        user_form = UserRegistrationForm()
        return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def profile_edit(request):
    """ Profile editing view """

    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль успешно обновлён')
        else:
            messages.error(request, 'Ошибка обновления профиля')

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'account/edit.html', context)
