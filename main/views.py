from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm, PortfolioForm
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy
from portfolio.models import Portfolio


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            return redirect('/profile.html')
    else:
        form = RegistrationForm()
    return render(request, 'registration/registration.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'portfolio/profile.html')


class CreatePortfolio(CreateView):
    model = Portfolio
    form_class = PortfolioForm
    template_name = 'index.html'
    success_url = reverse_lazy('index')

