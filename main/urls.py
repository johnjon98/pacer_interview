from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('get_score/', views.GetScoreView.as_view(), name='get_score'),
    

]