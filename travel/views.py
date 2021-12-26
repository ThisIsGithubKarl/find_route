from django.shortcuts import render


def home(request):
    context = {'name': 'Bob'}

    return render(request, 'home.html', context=context)


def about(request):
    return render(request, 'about.html')
