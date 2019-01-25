from django.urls import path

from . import views
from .views import ChartData, OutsideTempChartData
app_name = 'temo'
urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    path('test/', views.test_index, name='test'),
    path('add/', views.write, name='write'),
    path('on_click/', views.on_click, name='on_click'),
    # ex: /polls/5/results/
    # path('chart/', views.weather_chart_view, name='load_charts'),
    path('chart/data/', ChartData.as_view()),
    path('chart/temp/outside', OutsideTempChartData.as_view()),
    path('home/', views.home, name='home'),
    # ex: /polls/5/vote/
    #path('<int:question_id>/vote/', views.vote, name='vote'),

]
