from django.urls import path

from routes.views import *

urlpatterns = [
    path('detail/<int:pk>/', RouteDetailView.as_view(), name='detail'),
    path('delete/<int:pk>/', RouteDeleteView.as_view(), name='delete'),
    path('find/', RouteFindView.as_view(), name='find'),
    path('create/', add_route, name='create'),
    path('save/', save_route, name='save'),
    path('', RouteListView.as_view(), name='home'),
]
