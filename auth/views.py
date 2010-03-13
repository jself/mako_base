# Create your views here.
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from utils import render_to_response


def login(request):
    if request.method == "POST":
        next = request.POST.get("next", '/')
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth.login(request, form.get_user())
            messages.success(request, "You are now logged in.")
            return HttpResponseRedirect(next)
        else:
            request.session.set_test_cookie()
            messages.error(request, "There was an error logging you in.")
    else:
        request.session.set_test_cookie()
        next = request.GET.get("next", '/')
        form = AuthenticationForm(request)
    return render_to_response("auth/login.html", **{"form":form, "next":next})

def logout(request):
    auth.logout(request)
    messages.success(request, "You are now logged out.")
    next = request.GET.get("next", "/")
    return HttpResponseRedirect(next)

        
def register(request):
    if request.method == "POST":
        next = request.POST.get("next", "/")
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = auth.authenticate(username=user.username, password=form.cleaned_data['password1'])
            auth.login(request, user)
            messages.success(request, "New user created, you are now logged in.")
            return HttpResponseRedirect(next)
        messages.error(request, "There were errors in the form below.")
    else:
        next = request.GET.get("next", "/")
        form = UserCreationForm()
    return render_to_response("auth/register.html", form=form, next=next)

def forgot_pass(request):
    return HttpResponse("Not yet implemented")
