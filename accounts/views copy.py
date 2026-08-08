from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm


def login_view(request):

    if request.method == "POST":

        form = LoginForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(username=username, password=password)

            if user is not None:

                login(request, user)

                messages.success(request, "Login Successfull.")
                
                next_url = request.POST.get("next")

                if next_url:

                    return redirect(next_url)

                return redirect("dashboard:dashboard")
            else:

                messages.error(request, "Invalid username or password.")

    else:

        form = LoginForm()

    return render(request, "accounts/login.html", {
        "form": form
    })


def logout_view(request):
    
    if request.method == "POST":

        logout(request)

        messages.success(request, "You have been logged out successfully.")

    return redirect("accounts:login")
