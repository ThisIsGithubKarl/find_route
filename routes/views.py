from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, DetailView, CreateView, ListView, DeleteView

from cities.models import City
from routes.forms import RouteForm, RouteModelForm
from routes.models import Route
from routes.utils import get_routes

__all__ = (
    'find',
    'add_route',
    'save_route',
    'RouteFindView',
    'RouteDetailView',
    'RouteCreateView',
    'RouteListView',
    'RouteDeleteView',
)

from trains.models import Train


def find(request):
    form = RouteForm()
    context = {'form': form}
    return render(request, 'routes/find.html', context)


class RouteFindView(View):
    def get(self, request, *args, **kwargs):
        form = RouteForm()
        messages.error(request, "Неверный формат формы")
        context = {'form': form}
        return render(request, "routes/find.html", context)

    def post(self, request, *args, **kwargs):
        form = RouteForm(request.POST)
        if form.is_valid():
            try:
                context = get_routes(request, form)
            except ValueError as err:
                messages.error(request, err)
                context = {'form': form}
        return render(request, "routes/find.html", context)


def add_route(request):
    if request.method == "POST":
        data = request.POST
        if data:
            total_time = int(data['total_time'])
            from_city_id = int(data['from_city'])
            to_city_id = int(data['to_city'])
            trains = data['trains'].split()
            trains_list = [int(train) for train in trains if train.isdigit()]
            qs = Train.objects.filter(id__in=trains_list).select_related('from_city', 'to_city')
            cities = City.objects.filter(id__in=[from_city_id, to_city_id]).in_bulk()
            form = RouteModelForm(initial={
                    'from_city': cities[from_city_id],
                    'to_city': cities[to_city_id],
                    'travel_time': total_time,
                    'trains': qs
            })
            context = {'form': form}
        return render(request, 'routes/create.html', context)
    else:
        messages.error(request, "Нет маршрута для сохранения")
        return redirect('/')


def save_route(request):
    if request.method == "POST":
        form = RouteModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Маршрут успешно сохранен")
            return redirect('/')
        return render(request, 'routes/create.html', context={'form': form})
    else:
        messages.error(request, "Нет маршрута для сохранения")
        return redirect('/')
    
    
class RouteDetailView(DetailView):
    queryset = Route.objects.all()
    template_name = "Routes/details.html"


class RouteCreateView(SuccessMessageMixin, CreateView):
    model = Route
    form_class = RouteForm
    template_name = 'routes/create.html'
    success_url = reverse_lazy('routes:home')
    success_message = "Маршрут успешно создан"


class RouteListView(ListView):
    paginate_by = 9
    model = Route
    template_name = 'routes/home.html'


class RouteDeleteView(LoginRequiredMixin, DeleteView):
    model = Route
    template_name = 'routes/delete.html'
    success_url = reverse_lazy('routes:home')

    def post(self, request, *args, **kwargs):
        messages.success(request, "Маршрут успешно удален")
        return super().post(request, *args, **kwargs)
