from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from .forms import RegisterForm


class RegisterView(View):
    """
    View for user registration.
    This class-based view handles user registration. It includes methods to display the registration form,
    validate form input, and process registration requests.

    Attributes:
    template_name (str): The template name for the registration page.
    form_class (Form): The form class for user registration.

    Methods:
    dispatch(request, *args, **kwargs): Overrides the dispatch method to redirect authenticated users.
    get(request): Handles GET requests to display the registration form.
    post(request): Handles POST requests to process registration form submissions.
    """
    template_name = "users/signup.html"
    form_class = RegisterForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to="app_main:root")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            messages.success(
                request, f"Вітаємо, {username}!"
            )
            return redirect(to="users:signin")
        return render(request, self.template_name, {"form": form})
