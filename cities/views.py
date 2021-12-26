from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from cities.forms import HtmlForm, CityForm
from cities.models import City

__all__ = (
    'home',
    'CityDetailView',
    'CityCreateView',
    'CityUpdateView',
    'CityDeleteView',
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
    context = {'objects_list': qs, 'form': form}
    return render(request, "cities/home.html", context=context)


class CityDetailView(DetailView):
    queryset = City.objects.all()
    template_name = "cities/details.html"


class CityCreateView(CreateView):
    model = City
    form_class = CityForm
    template_name = 'cities/create.html'


class CityUpdateView(UpdateView):
    model = City
    form_class = CityForm
    template_name = 'cities/update.html'


class CityDeleteView(DeleteView):
    model = City
    template_name = 'cities/delete.html'
    success_url = reverse_lazy('cities:home')
