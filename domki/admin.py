from django.contrib import admin
from domki.models import House, Reservation

# Register your models here.

class HouseAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "is_reserved"]
    fields = ["name"]
    readonly_fields = ["is_reserved"]
    
admin.site.register(House, HouseAdmin)
admin.site.register(Reservation)
