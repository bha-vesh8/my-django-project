from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth import login as auth,logout
from minor.models import *
from django.contrib.auth.hashers import make_password , check_password
from django.views import View
from minor.middlewares.auth import simple_middleware
from django.utils.decorators import method_decorator
from django.conf import settings
import stripe
from django.http import JsonResponse
import requests
from django.db.models import Q
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

@login_required
@csrf_exempt  # Ensure CSRF middleware works
def book_appointment1(request):
    if request.method == 'POST':
        try:
            doctor_id = request.POST.get('doctor_id')
            appointment_date = request.POST.get('appointment_date')
            appointment_time = request.POST.get('appointment_time')

            if not doctor_id or not appointment_date or not appointment_time:
                return JsonResponse({'status': 'error', 'message': 'Missing required fields.'}, status=400)

            try:
                doctor = Doctors.objects.get(id=doctor_id)
            except Doctors.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Doctor not found.'}, status=404)

            date_obj = datetime.strptime(appointment_date, "%Y-%m-%d").date()
            time_obj = datetime.strptime(appointment_time, "%H:%M").time()

            if Appointment.objects.filter(doctor=doctor, date=date_obj, time=time_obj).exists():
                return JsonResponse({'status': 'error', 'message': 'Time slot already booked.'}, status=400)

            Appointment.objects.create(
                patient=request.user,
                doctor=doctor,
                date=date_obj,
                time=time_obj,
            )
            return JsonResponse({'status': 'success', 'message': 'Appointment booked successfully!'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'An error occurred: {str(e)}'}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

@login_required
def get_available_time_slots(request, doctor_id, date):
    try:
        selected_date = datetime.strptime(date, "%Y-%m-%d").date()
        start_time = datetime.strptime("09:00", "%H:%M")
        end_time = datetime.strptime("17:00", "%H:%M")
        interval = timedelta(minutes=30)

        booked_times = set(Appointment.objects.filter(
            doctor_id=doctor_id, date=selected_date
        ).values_list('time', flat=True))

        time_slots = []
        current_time = start_time
        while current_time < end_time:
            if current_time.time() not in booked_times:
                time_slots.append(current_time.strftime("%H:%M"))
            current_time += interval

        return JsonResponse({'time_slots': time_slots})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)






# Create your views here.

class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error_message = None

        customer = Customer(first_name=first_name,
                            last_name=last_name,
                            phone=phone,
                            email=email,
                            password=password)
        error_message = self.validateCustomer(customer)

        if not error_message:
            print(first_name, last_name, phone, email, password)
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('order')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html', data)

    def validateCustomer(self, customer):
        error_message = None;
        if (not customer.first_name):
            error_message = "First Name Required !!"
        elif len(customer.first_name) < 4:
            error_message = 'First Name must be 4 char long or more'
        elif not customer.last_name:
            error_message = 'Last Name Required'
        elif len(customer.last_name) < 4:
            error_message = 'Last Name must be 4 char long or more'
        elif not customer.phone:
            error_message = 'Phone Number required'
        elif len(customer.phone) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len(customer.password) < 6:
            error_message = 'Password must be 6 char long'
        elif len(customer.email) < 5:
            error_message = 'Email must be 5 char long'
        elif customer.isExists():
            error_message = 'Email Address Already Registered..'
        # saving

        return error_message    
       
    

class Login(View):
    return_url = None
    def get(self , request):
        Login.return_url = request.GET.get('return_url', request.META.get('HTTP_REFERER'))
        return render(request , 'loginn.html')

    def post(self , request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id

                if Login.return_url:
                    return_url = Login.return_url
                    Login.return_url = None
                    return HttpResponseRedirect(return_url) 
                else:
                    Login.return_url = None
                    return redirect('order')
            else:
                error_message = 'Email or Password invalid !!'
        else:
            error_message = 'Email or Password invalid !!'

        print(email, password)
        return render(request, 'loginn.html', {'error': error_message})

def logout(request):
    request.session.clear()
    return redirect('loginn')

def mypatient (request):
    print('you are :', request.session.get('username'))
    print('your email is :', request.session.get('email'))
    return render(request,'mypatient.html')

def ambulance (request):
    return render(request,'ambulance.html')

def health (request):
    return render(request,'health.html')

def about (request):
    return render(request,'about.html')

def home ():
    return redirect('mypatient')

def book_appointment (request):
    return render(request,'book_appointment.html')

class Index(View):
    
    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity-1
                else:
                    cart[product] = quantity+1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
            
        request.session['cart'] = cart
        print(request.session['cart'])
        
        return redirect('order')
    
    def get(self, request):
     cart = request.session.get('cart')
     if not cart:
         request.session['cart'] = {}
     categories = Categories.get_all_categories()
     all_products = Product.get_all_products()
     categories_with_products = []
     for category in categories:
        products = category.products.all()
        categories_with_products.append({
            'category': category,
            'products': products,
            
        })
    
     context = {
        'categories_with_products': categories_with_products,
        'all_products': all_products
     }
     return render(request,'order.html', context)
 
class cart(View):
    
    def get(self , request):
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        print(products)
        return render(request , 'cart.html' , {'products' : products})
    

class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        print(address, phone, customer, cart, products)

        for product in products:
            print(cart.get(str(product.id)))
            order = Order(customer=Customer(id=customer),
                          product=product,
                          price=product.price,
                          address=address,
                          phone=phone,
                          quantity=cart.get(str(product.id)))
            order.save()
        request.session['cart'] = {}

        return redirect('cart')
    
stripe.api_key = settings.STRIPE_API_KEY

    
def checkout_session(request):
    # Get cart from session (example: {product_id: quantity})
    cart = request.session.get('cart', {})

    # Fetch all products from the database that are in the cart
    products = Product.objects.filter(id__in=cart.keys())

    # Dynamically build the line_items array for Stripe
    line_items = []
    for product in products:
        line_items.append({
            'price_data': {
                'currency': 'inr',
                'unit_amount': int(product.price * 100),  # Price in cents
                'product_data': {
                    'name': product.name,  # Product name
                },
            },
            'quantity': cart[str(product.id)],  # Quantity from cart
        })

    # Create Stripe Checkout session
    try:
        session = stripe.checkout.Session.create(
            line_items=line_items,
            mode='payment',
            billing_address_collection='required',
            success_url='http://127.0.0.1:8000/success',
            cancel_url='http://127.0.0.1:8000/cancel',
        )
        return redirect(session.url, code=303)
    except stripe.error.StripeError as e:
        # Handle Stripe errors
        print(f"Error creating Stripe session: {e}")
        return redirect('cart')  # Or any fallback route

def success(request):
    return render(request,'success.html')

def cancel(request):
    return render(request,'cancel.html')
            

class Orders(View):
    
    @method_decorator(simple_middleware)
    def get(self, request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        print(orders)
        return render(request , 'orders.html'  , {'orders' : orders})
    
def search(request):
    query=request.GET.get('query')
    if query:
     data = Product.objects.filter(
        Q(name__icontains=query) | Q(category__name__icontains = query)
        ).order_by('-id')
    else:
        data = Product.objects.none() 
    return render(request, 'search.html',{'data' : data})

def d_search(request):
    d_query = request.GET.get('d_query')
    if d_query:
        d_data = Doctors.objects.filter(
            Q(name__icontains=d_query) | Q(specialist__name__icontains=d_query)
        ).order_by('-id')
    else:
        d_data = Doctors.objects.none()
    
    # Group doctors by specialist for the template
    specialist_with_doctors = {}
    for doctor in d_data:
        specialist = doctor.specialist
        if specialist not in specialist_with_doctors:
            specialist_with_doctors[specialist] = []
        specialist_with_doctors[specialist].append(doctor)
    
    context = {
        'd_query': d_query,
        'specialist_with_doctors': specialist_with_doctors.items(),
    }
    return render(request, 'doctorsearch.html', context)


OPENCAGE_API_KEY = '31610de934234eeb9740d5100eb7dfb5'
def book_ambulance(request):
        if request.method == 'POST':
        # Get latitude and longitude from the form
         latitude = request.POST.get('latitude')
         longitude = request.POST.get('longitude')

        # Call OpenCage API for reverse geocoding
         if latitude and longitude:
             url = f'https://api.opencagedata.com/geocode/v1/json?q={latitude}+{longitude}&key={OPENCAGE_API_KEY}'
             response = requests.get(url)
             data = response.json()

             if data['results']:
                address = data['results'][0]['formatted']
             else:
                address = "Address not found"

            # Process the form data and address as needed
             return render(request, 'confirmation.html', {
                'latitude': latitude,
                'longitude': longitude,
                'address': address
            })
         else:
          return JsonResponse({'error': 'Invalid latitude or longitude'}, status=400)

        return render(request, 'booking.html')


class Index1(View):
    
    def get(self, request):
     specialists = Specialist.get_all_specialist()
     all_doctors = Doctors.get_all_doctors()
     specialist_with_doctors = []
     for specialist in specialists:
        doctors = specialist.doctors.all()
        specialist_with_doctors.append({
            'specialist': specialist,
            'doctors': doctors,
            
        })
    
     context = {
        'specialist_with_doctors': specialist_with_doctors,
        'all_doctors': all_doctors
     }
     return render(request,'book_appointment.html', context)




