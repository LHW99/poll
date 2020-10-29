from django.urls import path

from . import views

app_name = 'app_polls'

# Django's DetailViews expect the primary key value captured from the url to be pk

urlpatterns = [
  path('', views.IndexView.as_view(), name='index'),
  path('<int:pk>/', views.DetailView.as_view(), name='detail'),
  path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
  path('<int:question_id>/vote/', views.vote, name='vote')
]