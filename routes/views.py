from django.shortcuts import render
from django.views.generic import View
from django.contrib import messages
from routes.forms import RouteForm

__all__ = (
    'home',
    'RouteView'
)


def home(request):
    form = RouteForm()
    context = {'form': form}
    return render(request, 'routes/home.html', context)


class RouteView(View):
    def get(self, request, *args, **kwargs):
        form = RouteForm()
        messages.error(request, "Неверный формат формы")
        context = {'form': form}
        return render(request, "routes/home.html", context)

    def post(self, request, *args, **kwargs):
        form = RouteForm(request.POST)
        context = {'form': form}
        return render(request, "routes/home.html", context)
