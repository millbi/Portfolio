from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from .models import Portfolio, Likes
from main.forms import ProfileUpdateForm, PortfolioForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    CreateView,
    UpdateView
)


def index(request):
    portfolios = Portfolio.objects.prefetch_related('subjects')
    result = []
    for pf in portfolios:
        subjects = [subject.name for subject in pf.subjects.all()]
        result.append({'main_image': pf.main_image, 'id': pf.id, 'title': pf.title, 'description': pf.description,
                       'subjects': subjects})
    return render(request, 'portfolio/index.html', {'portfolios': result})


def about(request):
    return render(request, 'portfolio/about.html')


@login_required
def profile(request):
    if request.method == 'GET':
        return render(request, 'portfolio/profile.html', {'update_form': ProfileUpdateForm()})
    else:
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            return redirect('profile.html')


class PortfolioDetail(View):
    def get(self, request, pk):
        portfolio = Portfolio.objects.get(id=pk)
        return render(request, 'portfolio/pf_detail.html', {'portfolio': portfolio})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class AddLike(View):
    def get(self, request, pk):
        ip_client = get_client_ip(request)
        try:
            Likes.objects.get(ip=ip_client, pos_id=pk)
            return redirect(f'/{pk}')
        except:
            new_like = Likes()
            new_like.ip = ip_client
            new_like.pos_id = int(pk)
            new_like.save()
            return redirect(f'/{pk}')


class DelLike(View):
    def get(self, request, pk):
        ip_client = get_client_ip(request)
        try:
            lik = Likes.objects.get(ip=ip_client, pos_id=pk)
            lik.delete()
            return redirect(f'/{pk}')
        except:
            return redirect(f'/{pk}')


class PortfolioUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Portfolio
    fields = ['title', 'description']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        portfolio = self.get_object()
        if self.request.user == portfolio.user:
            return True
        return False


class PortfolioCreateView(LoginRequiredMixin, CreateView):
    model = Portfolio
    fields = ['title', 'description']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def create_portfolio(request):
    if request.method == 'GET':
        return render(request, 'portfolio/create_portfolio.html', {'create_form': PortfolioForm()})
    else:
        new_portfolio = Portfolio()
        new_portfolio.profile = request.user.profile
        form = PortfolioForm(request.POST, request.FILES, new_portfolio)
        if form.is_valid():
            form.save()
        return redirect('index')
