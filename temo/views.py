from django.http import HttpResponse

from .models import Reading, Sensor, ReadDate
from django.utils import timezone
import datetime

from django.shortcuts import render, render_to_response


from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q

LAST_READINGS = []
readings_bufor = []

sensor_names = {sensor.id: sensor.name for sensor in Sensor.objects.all()}
sensor_units = {sensor.id: str(sensor.unit) for sensor in Sensor.objects.all()}

last_write_db_time = [timezone.now()]

from django import template
register = template.Library()


def on_click(request):
    print('click')
    return HttpResponse("It was click")


def _prepare_index_context():
    if readings_bufor:
        last_write = readings_bufor[-1]
        return {
            'time': last_write['time'],
            'readings': [{
                'sensor_name': sensor_names[reading['id']],
                'value': reading['value'],
                'unit': sensor_units[reading['id']]} for reading in last_write['readings']]
        }
    else:
        return None


def index(request):
    return render(request, 'temo/index.html', _prepare_index_context())


def test_index(request):
    return render(request, 'temo/index.html', _prepare_index_context())


def write(request):
    zip_list = zip(request.POST.getlist('sensor_id'), request.POST.getlist('value'))

    buffor_dict = {
        'time': timezone.now(),
        'readings': [{'id': int(_id), 'value': val} for _id, val in zip_list]
    }
    readings_bufor.append(buffor_dict)

    if len(readings_bufor) > 301:
        readings_bufor.pop(0)

    if readings_bufor and readings_bufor[-1]['time'] - datetime.timedelta(minutes=5) > last_write_db_time[0]:
        for reading in readings_bufor[-1]['readings']:
            sensor = Sensor.objects.get(id=reading['id'])
            Reading.objects.create(sensor=sensor, value=reading['value'])
        last_write_db_time.append(timezone.now())
        last_write_db_time.pop(0)


    return HttpResponse("It was sent %s")


def home(request):
    return render_to_response('temo/load_charts.html', {'variable': 'world'})


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        outside_temp = Reading.objects.filter(sensor_id=2).order_by('-read_date').values()[:300:8]
        heater_temp = Reading.objects.filter(sensor_id=3).order_by('-read_date').values()[:300:8]
        boiler_temp = Reading.objects.filter(sensor_id=4).order_by('-read_date').values()[:300:8]

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
        readings = Reading.objects.filter(Q(sensor_id=4) | Q(sensor_id=3) | Q(sensor_id=2)).order_by(
            '-read_date_id').values('read_date_id', 'value')[:300:12]

        for reading in readings:
            print(reading)

        # data = {
        #     'date_time': date_list,
        #     'outside_temp': outside_temp_list
        # }
        print(readings)

        return Response(data)