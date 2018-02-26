from django.urls import path

from . import views
from .views import ChartData, OutsideTempChartData
app_name = 'temo'
urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('add/', views.write, name='write'),
    # ex: /polls/5/results/
    # path('chart/', views.weather_chart_view, name='load_charts'),
    path('chart/data/', ChartData.as_view()),
    path('chart/temp/outside', OutsideTempChartData.as_view()),
    path('home/', views.home, name='home'),
    # ex: /polls/5/vote/
    #path('<int:question_id>/vote/', views.vote, name='vote'),

]
