from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render

from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView

from images.models import Image
from trip.forms import AddTripForm
from trip.models import Trip
from trip.utils import generate_unique_slug, DataMixin


class AboutHikingapp(TemplateView):
    template_name = 'trip/about.html'


class TripList(DataMixin, ListView):
    template_name = 'trip/index.html'
    context_object_name = 'trips'
    title_page = 'Main page'

    def get_queryset(self):
        return (Trip.objects.filter(published=True).
                select_related('category', 'user').
                prefetch_related('user', 'tag'))


class ShowTrip(DetailView):
    model = Trip
    template_name = 'trip/trip.html'
    context_object_name = 'trip'

    def get_queryset(self):
        return (Trip.objects.filter().
                select_related('category', 'user').
                prefetch_related('user', 'tag'))

    def get_success_url(self):
        return reverse('trip', kwargs={'slug': self.object.slug})

    # def get_object(self, queryset=None):
    #     return get_object_or_404(Trip, slug=self.kwargs[self.slug_url_kwarg])


class AddTrip(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddTripForm
    template_name = 'trip/add.html'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        f = form.save()
        title = form.cleaned_data['title']
        f.slug = generate_unique_slug(Trip, title)
        images = form.cleaned_data['image']
        f.user = self.request.user

        if images:
            for i in images:
                Image.objects.create(image=i, travel=f)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('trip', kwargs={'slug': self.object.slug})


class EditTrip(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Trip
    template_name = 'trip/add.html'
    form_class = AddTripForm

    def get_queryset(self):
        return (Trip.objects.filter().
                select_related('user').
                prefetch_related('user'))

    # trip = get_object_or_404(Trip, user=self.request.user)

    # def get_object(self, queryset=None):
    #     print(self.request.FILES[1])
    #     t = Trip.objects.filter(user=self.request.user).select_related('user').prefetch_related('user')
    #     return Trip.objects.filter(user=self.request.user).select_related('user').prefetch_related('user')
    # # def get_queryset(self):
    #     return Trip.objects.filter(user=self.request.user).select_related('user').prefetch_related('user')

    def test_func(self):
        return (self.request.user == self.get_object().user) or self.request.user.is_superuser

    def form_valid(self, form):
        f = form.save()
        images = form.cleaned_data['image']

        if images:
            for i in images:
                Image.objects.create(image=i, travel=f)

        return super().form_valid(form)


class DeleteTrip(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Trip
    template_name = 'trip/delete.html'
    success_url = reverse_lazy('home')

    def get_queryset(self):
        return (Trip.objects.filter(slug=self.kwargs['slug']).
                select_related('user').
                prefetch_related('user'))

    def test_func(self):
        return (self.request.user == self.get_object().user) or self.request.user.is_superuser


class SearchTrip(ListView):
    template_name = 'trip/index.html'
    context_object_name = 'trips'

    def get_queryset(self):
        return (Trip.objects.filter(title__icontains=self.request.GET.get('search')).
                select_related('category').
                prefetch_related('user', 'tag'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search')
        return context


def handler_403(request, exception):
    return render(request, template_name='trip/403_csrf.html')


def handler_404(request, exception):
    return render(request, template_name='trip/404.html')


def handler_500(request):
    return render(request, template_name='trip/500.html')


def terms_of_use(request):
    return render(request, template_name='trip/terms_of_use.html')
