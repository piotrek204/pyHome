from django.contrib import admin

from .models import Reading, Sensor, Factor, Unit, ReadDate

admin.site.register(Reading)
admin.site.register(Sensor)
admin.site.register(ReadDate)
admin.site.register(Factor)
admin.site.register(Unit)