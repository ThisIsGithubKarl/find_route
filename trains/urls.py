from django.urls import path

from trains.views import *

urlpatterns = [
    path('detail/<int:pk>/', TrainDetailView.as_view(), name='detail'),
    path('update/<int:pk>', TrainUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', TrainDeleteView.as_view(), name='delete'),
    path('create/', TrainCreateView.as_view(), name='create'),
    path('', TrainListView.as_view(), name='home'),
]
