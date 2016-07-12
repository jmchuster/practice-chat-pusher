from django.template.response import TemplateResponse
from django.http import HttpResponseServerError
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect


class LoginView(View):
    def get(self, request):
        return TemplateResponse(request, 'login.html')

    def post(self, request):
        username = request.POST['inputUsername']
        password = request.POST['inputPassword']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect('index')
        else:
            return HttpResponseServerError('Incorrect username or password')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')

class SignupView(View):
    def get(self, request):
        return TemplateResponse(request, 'signup.html')

    def post(self, request):
        username = request.POST['inputUsername']
        password = request.POST['inputPassword']
        confirmation = request.POST['inputConfirmation']

        if password == confirmation:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            user = authenticate(username, password)
            if user is not None and user.is_active:
                login(request, user)
                return redirect('index')
            else:
                return HttpResponseServerError('There was an error creating your account')
        else:
            return HttpResponseServerError('Passwords must match')
