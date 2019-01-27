from django.db import models
import datetime
from django.utils import timezone


class Unit(models.Model):
    unit = models.CharField(max_length=20, default="C")

    def __str__(self):
        return self.unit


class Sensor(models.Model):
    name = models.CharField(max_length=200)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Factor(models.Model):
    multiplier = models.IntegerField(default=1)

    def __str__(self):
        return str(self.multiplier)


class ReadDate(models.Model):
    date = models.DateTimeField('Date read', null=True)

    def __str__(self):
        return str(self.date)


class Reading(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    read_date = models.ForeignKey(ReadDate, on_delete=models.CASCADE, editable=False, null=True)
    # factor = models.ForeignKey(Factor, on_delete=models.CASCADE, default=1)
    value = models.FloatField(default=0)

    def __str__(self):
        return ('%s: %s = %s%s' % (self.read_date, self.sensor.name, self.value, self.sensor.unit))

    def save(self, *args, **kwargs):
        read_date_dict = ReadDate.objects.order_by('-date').values()[0]
        if timezone.now() - read_date_dict['date'] <= datetime.timedelta(seconds=1):
            self.read_date = ReadDate.objects.order_by('-date')[0]
        else:
            self.read_date = ReadDate.objects.create(date=timezone.now())


        return super(Reading, self).save(*args, **kwargs)
