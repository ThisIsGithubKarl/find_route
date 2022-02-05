from django import forms

from cities.models import City
from routes.models import Route
from trains.models import Train


class RouteForm(forms.Form):
    from_city = forms.ModelChoiceField(label='Откуда', queryset=City.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control js-example-basic-single',
        'style': 'width: 25rem;',
    }))
    to_city = forms.ModelChoiceField(label='Куда', queryset=City.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control js-example-basic-single',
        'style': 'width: 25rem;',
    }))
    cities = forms.ModelMultipleChoiceField(label='Через города',
                                            queryset=City.objects.all(),
                                            required=False,
                                            widget=forms.SelectMultiple(attrs={
                                                'class': 'form-control js-example-basic-multiple',
                                                'style': 'width: 25rem;',
                                            }))
    travel_time = forms.IntegerField(label='Время в пути', required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Время в пути',
        'style': 'width: 25rem;',
    }))


class RouteModelForm(forms.ModelForm):
    name = forms.CharField(label='Название маршрута', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Название маршрута',
    }))
    from_city = forms.ModelChoiceField(label='Откуда', queryset=City.objects.all(), widget=forms.HiddenInput())
    to_city = forms.ModelChoiceField(label='Куда', queryset=City.objects.all(), widget=forms.HiddenInput())
    trains = forms.ModelMultipleChoiceField(label='Через города',
                                            queryset=Train.objects.all(),
                                            required=False,
                                            widget=forms.SelectMultiple(attrs={
                                                'class': 'form-control d-none',
                                                'style': 'width: 25rem;',
                                            }))
    travel_time = forms.IntegerField(label='Время в пути', required=False, widget=forms.HiddenInput())

    class Meta:
        model = Route
        fields = '__all__'
