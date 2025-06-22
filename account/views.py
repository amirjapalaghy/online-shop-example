from django.contrib.auth import login, authenticate, logout
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.views import View
from ghasedakpack import Ghasedak
from random import randint

from account.models import User, Otp
from .forms import LoginForm, RegisterForm, CheckOtpForm

SMS = Ghasedak('30144696d43ac2188d91293b554a3925166b897de938ad8bb09909448acf40d6kkThPKhLWhQZVoZt')


class UserLoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home:home')
        return render(request, 'account/login.html', {'form': form})


class RegisterView(View):

    def get(self, request):
        form = RegisterForm()
        return render(request, 'account/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():

            randcode = randint(10000, 99999)
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            request.session['password'] = password
            request.session['phone'] = phone
            # SMS.verification(
            #     {'receptor': phone, 'type': '1',
            #      'templates': 'randcode', 'param1': randcode}
            # )
            Otp.objects.create(phone=phone, code=randcode)
            print(randcode)
            return redirect('account:check_otp')
        else:
            form.add_error('phone', 'invalid phone')

        return render(request, 'account/register.html', {'form': form})


class CheckOtpView(View):
    def get(self, request):
        form = CheckOtpForm()
        return render(request, 'account/check_otp.html', {'form': form})

    def post(self, request):
        form = CheckOtpForm(request.POST)
        if form.is_valid():
            phone = request.session['phone']
            password = request.session['password']
            request.session['password'] = {}
            request.session['phone'] = {}
            code = form.cleaned_data['code']
            if Otp.objects.filter(code=code, phone=phone).exists():
                user = User.objects.create_user(phone=phone, password=password)
                login(request, user)
                Otp.delete(Otp.objects.get(code=code, phone=phone))
                return redirect('home:home')
        else:
            form.add_error('phone', 'invalid phone')

        return render(request, 'account/register.html', {'form': form})


def logout_user(request):
    if request.method == 'GET':
        logout(request)
        return redirect('home:home')

