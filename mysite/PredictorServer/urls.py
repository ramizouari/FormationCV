from django.urls import path

from . import views

urlpatterns = [
    path('', views.predict, name='predict'),
    path('detailed', views.predict_detailed, name='predict_detailed'),
    path('minimal', views.predict_min, name='predict_min'),

]