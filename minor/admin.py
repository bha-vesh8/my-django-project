from django.contrib import admin
from minor.models import *


class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']
    
    
class AdminCategory(admin.ModelAdmin):
    list_display = ['name']
    
class AdminDoctor(admin.ModelAdmin):
    list_display = ['name', 'age', 'specialist', 'address']
    
    
class AdminSpecialist(admin.ModelAdmin):
    list_display = ['name']
    
class appointment(admin.ModelAdmin):
    list_display = ['patient', 'doctor']
    
    
# Register your models here.
admin.site.register(Product, AdminProduct)
admin.site.register(Categories, AdminCategory)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Booking)
admin.site.register(Doctors, AdminDoctor)
admin.site.register(Specialist, AdminSpecialist)
admin.site.register(Appointment, appointment)