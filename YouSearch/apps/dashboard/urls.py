from django.conf.urls import url
from django.urls import path
from apps.dashboard import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.main, name='main'),
    path(r'paper_id=<paper_id>', views.get_similar_papers, name='get_similar')
]