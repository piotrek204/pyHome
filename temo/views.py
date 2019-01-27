from django.shortcuts import render
from django.http import HttpResponse

from .models import Reading, Sensor, ReadDate
from django.utils import timezone
import datetime

from django.http import Http404
from django.shortcuts import get_object_or_404, render, render_to_response
from chartit import DataPool, Chart


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.db.models import F
from django.db.models import Q

LAST_READINGS = []
LIVE_DATA = [None]
SENSOR_NAME = ['Temperatura pieca', 'Temperatura boilera', 'Temperatura zewnetrzna', 'Temperatura salon']
SENSOR_UNIT = ['C', 'C', 'C', 'C']
readings_bufor = []

sensor_names = {sensor.id: sensor.name for sensor in Sensor.objects.all()}
sensor_units = {sensor.id: str(sensor.unit) for sensor in Sensor.objects.all()}


from django import template
register = template.Library()


def on_click(request):
    print('click')
    return HttpResponse("It was click")


def index(request):
    try:
        context = readings_bufor[-1]
    except:
        context = None
    return render(request, 'temo/index.html', context)


def test_index(request):
    latest_readings = Reading.objects.order_by('-read_date')[:4]  # order_by('-pub_date')[:5]
    context = {'latest_readings': latest_readings, 'live_data': LIVE_DATA[-1], 'data_time': timezone.now()}
    return render(request, 'temo/test.html', context)


def write(request):
    id_list = request.POST.getlist('sensor_id')
    value_list = request.POST.getlist('value')
    zip_list = zip(id_list, value_list)

    bufor_dict = {
        'time': timezone.now(),
        'readings': [
            {'sensor_name': sensor_names[int(_id)],
             'value': val,
             'unit': sensor_units[int(_id)]} for _id, val in zip_list
        ]
    }
    readings_bufor.append(bufor_dict)

    if len(readings_bufor) > 301:
        readings_bufor.pop(0)

    if readings_bufor and readings_bufor[-1]['time'] - datetime.timedelta(minutes=5) > readings_bufor[0]['time']:
        for reading in readings_bufor[-1]['readings']:  # refactor is needed
            id = [key for key, value in sensor_names.items() if value == reading['sensor_name']][0]
            sensor = Sensor.objects.get(id=id)
            print('sensor', sensor)
            r = Reading.objects.create(sensor=sensor, value=reading['value'])
            print(r)
        print('zapisalem do bazy')


    return HttpResponse("It was sent %s")


def home(request):
    return render_to_response('temo/load_charts.html', {'variable': 'world'})


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        # reading = Reading.objects.values_list('read_date', 'value').filter(sensor_id=2).order_by('-read_date')[:7]
        outside_temp = Reading.objects.filter(sensor_id=4).order_by('-read_date').values()[:300:8]
        # print(outside_temp)
        heater_temp = Reading.objects.filter(sensor_id=2).order_by('-read_date').values()[:300:8]
        boiler_temp = Reading.objects.filter(sensor_id=3).order_by('-read_date').values()[:300:8]

        outside_temp_list = []
        heater_temp_list = []
        boiler_temp_list = []
        date_list = []
        for outside, heater, boiler in zip(outside_temp, heater_temp, boiler_temp):
            outside_temp_list.insert(0,outside['value'])
            heater_temp_list.insert(0,heater['value'])
            boiler_temp_list.insert(0,boiler['value'])
            read_date = ReadDate.objects.get(id=outside['read_date_id'])
            date_list.insert(0,read_date.date)
        data = {'date_time': date_list,
                'outside_temp': outside_temp_list,
                'heater_temp': heater_temp_list,
                'boiler_temp': boiler_temp_list
                }

        return Response(data)


class OutsideTempChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        data = 0
        readings = Reading.objects.filter(Q(sensor_id=1) | Q(sensor_id=2) | Q(sensor_id=3)).order_by(
            '-read_date_id').values('read_date_id', 'value')[:300:12]

        for reading in readings:
            print(reading)

        # data = {
        #     'date_time': date_list,
        #     'outside_temp': outside_temp_list
        # }
        print(readings)

        return Response(data)