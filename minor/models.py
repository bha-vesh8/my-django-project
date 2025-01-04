from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=500)

    def register(self):
        self.save()

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False


    def isExists(self):
        if Customer.objects.filter(email = self.email):
            return True

        return  False
    
class Categories(models.Model):
    name = models.CharField(max_length=20)
    
    @staticmethod
    def get_all_categories():
        return Categories.objects.all()
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Categories, related_name='products', on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=200, default='', null = True, blank=True)
    image = models.ImageField(upload_to='uploads/products/')
    
    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in =ids)
    
    @staticmethod
    def get_all_products():
        return Product.objects.all()
    
    @staticmethod
    def get_all_products_by_id(category_id):
        return Product.objects.filter(category = category_id)

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=50, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    date = models.DateField(default=datetime.today)
    status = models.BooleanField(default = False)
    
    
    def placeorder(self):
        self.save()
        
    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order \
            .objects \
            .filter(customer=customer_id) \
            .order_by('-date')
            
class Booking(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.name}"
    
# ======================= Doctors ===================
class Specialist(models.Model):
    name = models.CharField(max_length=20)
    
    @staticmethod
    def get_all_specialist():
        return Specialist.objects.all()
    
    def __str__(self):
        return self.name
    
class Doctors(models.Model):
    name = models.CharField(max_length=50)
    specialist = models.ForeignKey(Specialist, related_name='doctors', on_delete=models.CASCADE, default=1)
    age = models.CharField(max_length=3)
    address = models.CharField(max_length=50)
    description = models.CharField(max_length=1000, default='', null = True, blank=True)
    image = models.ImageField(upload_to='uploads/doctors/')
    
    @staticmethod
    def get_doctord_by_id(ids):
        return Doctors.objects.filter(id__in =ids)
    
    @staticmethod
    def get_all_doctors():
        return Doctors.objects.all()
    
    @staticmethod
    def get_all_doctors_by_id(specialist_id):
        return Doctors.objects.filter(specialist = specialist_id)
    
class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.patient.username} - {self.doctor.name} on {self.date} at {self.time}"
        
