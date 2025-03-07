from django.urls import path
from .views import *

urlpatterns = [
    path('', hello_world),
    path('complaints/', get_all_complaints, name='get_all_complaints'),
]
