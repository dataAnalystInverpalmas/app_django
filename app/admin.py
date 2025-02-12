from django.contrib import admin
from .models import Area, Date, Farm, Flower, Group, GroupFlowers, Production, SubGroup, Record, DataType


admin.site.register(Area)
admin.site.register(Date)
admin.site.register(Farm)
admin.site.register(Flower)
admin.site.register(Group)
admin.site.register(GroupFlowers)
admin.site.register(Production)
admin.site.register(SubGroup)
admin.site.register(Record)
admin.site.register(DataType)