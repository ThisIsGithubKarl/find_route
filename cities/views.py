from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from django.core.paginator import Paginator

from cities.forms import HtmlForm, CityForm
from cities.models import City

__all__ = (
    'home',
    'CityDetailView',
    'CityCreateView',
    'CityUpdateView',
    'CityDeleteView',
    'CityListView',
)


def home(request, pk=None):
    # if pk is not None:
    #     # city = City.objects.filter(pk=pk).first()
    #     # city = City.objects.get(pk=pk)
    #     city = get_object_or_404(City, pk=pk)
    #
    #     context = {'object': city}
    #     return render(request, "cities/details.html", context=context)

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()

    form = CityForm()

    qs = City.objects.all()
    pg_list = Paginator(qs, 10)
    page_number = request.GET.get('page')
    page_obj = pg_list.get_page(page_number)

    context = {'page_obj': page_obj, 'form': form}
    return render(request, "cities/home.html", context=context)


class CityDetailView(DetailView):
    queryset = City.objects.all()
    template_name = "cities/details.html"


class CityCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = City
    form_class = CityForm
    template_name = 'cities/create.html'
    success_url = reverse_lazy('cities:home')
    success_message = "Город успешно создан"


class CityUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = City
    form_class = CityForm
    template_name = 'cities/update.html'
    success_url = reverse_lazy('cities:home')
    success_message = "Город успешно отредактирован"


class CityDeleteView(LoginRequiredMixin, DeleteView):
    model = City
    template_name = 'cities/delete.html'
    success_url = reverse_lazy('cities:home')

    def post(self, request, *args, **kwargs):
        messages.success(request, "Город успешно удален")
        return super().post(request, *args, **kwargs)


class CityListView(ListView):
    paginate_by = 10
    model = City
    template_name = 'cities/home.html'
