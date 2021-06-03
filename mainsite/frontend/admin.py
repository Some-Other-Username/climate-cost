from django.contrib import admin

from .models import *

admin.site.register(Region)
admin.site.register(Reference)
admin.site.register(Restriction)

admin.site.register(UnitType)
admin.site.register(UnitConversion)

admin.site.register(LifeCycleStage)

admin.site.register(EmissionType)
admin.site.register(EmissionConversion)
admin.site.register(Emission)

admin.site.register(ItemCategory)
