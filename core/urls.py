"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from minor.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup', Signup.as_view(), name="signup"),
    path('loginn/', Login.as_view(), name="loginn"),
    path('', mypatient, name="mypatient"),
    path('', home, name="home"),
    path('logout/', logout, name="logout"),
    path('ambulance/', ambulance, name='ambulance'),
    path('health/', health, name='health'),
    path('about/', about, name='about'), 
    path('order/', Index.as_view(), name='order'),
    path('search', search, name='search'),
    path('doctorsearch', d_search, name='d_search'),
    path('cart/', cart.as_view(), name='cart'),
    path('check-out', CheckOut.as_view(), name='checkout'),
    path('checkout_session', checkout_session, name='checkout_session'),
    path('success', success, name='success'),
    path('cancel', cancel, name='cancel'),
    path('orders', Orders.as_view(), name='Orders'),
    path('book', book_ambulance, name='book_ambulance'),
    path('book_appointment/', Index1.as_view(),name='book_appointment'),
    path('available-time-slots/<int:doctor_id>/<str:date>/', get_available_time_slots, name='available_time_slots'),
    path('book-appointment/', book_appointment1, name='book_appointment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)