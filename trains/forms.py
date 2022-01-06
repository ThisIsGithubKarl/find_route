from django import forms

from trains.models import Train


class TrainForm(forms.ModelForm):
    # name = forms.CharField(label='Город', widget=forms.TextInput(attrs={
    #     'class': 'form-control',
    #     'placeholder': 'Введите название города'
    # }))

    class Meta:
        model = Train
        fields = ('name', 'from_city', 'to_city', 'travel_time')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название маршрута',
            }),
            'from_city': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Выберите пункт отправления',
            }),
            'to_city': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Выберите пункт назначения',
            }),
            'travel_time': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Укажите время в пути',
            }),
        }
        # labels = {
        #     'name': forms.CharField(attrs={
        #         'class': 'form-control'
        #     })
        # }
