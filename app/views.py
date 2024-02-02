from django.shortcuts import render, HttpResponse,redirect
from django.views import View
from django.urls import reverse
from .scrap import getEmails
from django.http import HttpResponse
from .models import Restaurant, Customer, Order, Item, Payment
from datetime import datetime
import pytz
from django.db.models import Count, Sum
from django.contrib import messages
from .charts_functions import orders_by_status,quantity_by_item, orders_over_time
from .forms import (CustomerRegistrationForm)

from django.db import IntegrityError

def get_chart(request):
    try:
        chart_data = {
            'chart_1': {'orders_by_status_data': orders_by_status(request)},
            'chart_2' : {'quantity_by_item_data':quantity_by_item(request)},
            'chart_3' : {'orders_over_time':orders_over_time(request)}
        }
        # print('chart_data----->',chart_data.get('chart_3'))
        return render(request, 'app/order_chart.html', {'chart_data': chart_data})
    except Exception as e:
        # Handle exceptions gracefully
        error_message = f"An error occurred: {str(e)}"
        return HttpResponse(error_message)
        # return render(request, 'error.html', {'error_message': error_message})

def scrap_swiggy_data(request):

    return render(request,'app/scrap.html')

# def successfully_scrap2(request):
#     received_data = getEmails()  # received_data contains the list with data
#     print(received_data)

#     for data in received_data:
#         # Create and save the Restaurant object

#         if 'not found' in data['restaurant']['restaurant_name'].lower() or \
#            'not found' in data['restaurant']['restaurant_address'].lower() or \
#            'not found' in data['customer_info']['customer_name'].lower() or \
#            'not found' in data['customer_info']['customer_address'].lower() or \
#            'not found' in data['order_data']['Order No:'].lower() or \
#            'not found' in data['order_data']['Order placed at:'].lower() or \
#            'not found' in data['order_data']['Order delivered at:'].lower() or \
#            'not found' in data['order_data']['Order Status'].lower() or \
#            'not found' in str(data['order_summary']['Order Total']).lower():
#             continue


#         restaurant = Restaurant.objects.create(
#             rname=data['restaurant']['restaurant_name'],
#             raddress=data['restaurant']['restaurant_address']
#         )

#         # Create and save the Customer object
#         customer = Customer.objects.create(
#             cname=data['customer_info']['customer_name'],
#             caddress=data['customer_info']['customer_address']
#         )

#         # Create and save the Order object
#         order = Order.objects.create(
#             order_number=data['order_data']['Order No:'],
#             order_placed_at=datetime.strptime(data['order_data']['Order placed at:'], '%A, %B %d, %Y %I:%M %p').replace(tzinfo=pytz.UTC),
#             order_delivered_at=datetime.strptime(data['order_data']['Order delivered at:'], '%A, %B %d, %Y %I:%M %p').replace(tzinfo=pytz.UTC),
#             order_status=data['order_data']['Order Status'],
#             restaurant=restaurant,
#             customer=customer,
#             order_total=data['order_summary']['Order Total']
#         )

#         # Create and save the Item objects
#         for item in data['item_details']:
#             Item.objects.create(
#                 order=order,
#                 iname=item[0],
#                 quantity=item[1],
#                 price=item[2],
#                 itotal=item[1]*item[2]
#             )

#         # Create and save the Payment object
#         Payment.objects.create(
#             order=order,
#             payment_method='Unknown',  # Update this as per your data
#             items_total=data['order_summary']['Item Total'],
#             packing_charges=data['order_summary']['Order Packing Charges'],
#             platform_fee=data['order_summary']['Platform fee'],
#             delivery_partner_fee=data['order_summary']['Delivery partner fee'],
#             discount_applied=data['order_summary']['Discount Applied'],
#             taxes=data['order_summary']['Taxes'],
#             order_total=data['order_summary']['Order Total']
#         )

#     return HttpResponse("Data successfully added")


# def successfully_scrap3(request):
#     received_data = getEmails()  # received_data contains the list with data
#     print(received_data)

#     for data in received_data:
#         # Check if any field contains 'not found'
#         if 'not found' in data['restaurant']['restaurant_name'].lower() or \
#            'not found' in data['restaurant']['restaurant_address'].lower() or \
#            'not found' in data['customer_info']['customer_name'].lower() or \
#            'not found' in data['customer_info']['customer_address'].lower() or \
#            'not found' in data['order_data']['Order No:'].lower() or \
#            'not found' in data['order_data']['Order placed at:'].lower() or \
#            'not found' in data['order_data']['Order delivered at:'].lower() or \
#            'not found' in data['order_data']['Order Status'].lower() or \
#            'not found' in str(data['order_summary']['Order Total']).lower():
#             continue

#         # Check if the Restaurant object exists, if not create a new one
#         restaurant, created = Restaurant.objects.get_or_create(
#             rname=data['restaurant']['restaurant_name'],
#             raddress=data['restaurant']['restaurant_address']
#         )

#         if not created:
#             continue

#         # Check if the Customer object exists, if not create a new one
#         customer, created = Customer.objects.get_or_create(
#             cname=data['customer_info']['customer_name'],
#             caddress=data['customer_info']['customer_address']
#         )

#         if not created:
#             continue

#         # Create and save the Order object
#         order_placed_at = datetime.strptime(data['order_data']['Order placed at:'], '%A, %B %d, %Y %I:%M %p').replace(tzinfo=pytz.UTC) if 'not found' not in data['order_data']['Order placed at:'].lower() else None
#         order_delivered_at = datetime.strptime(data['order_data']['Order delivered at:'], '%A, %B %d, %Y %I:%M %p').replace(tzinfo=pytz.UTC) if 'not found' not in data['order_data']['Order delivered at:'].lower() else None

#         order = Order.objects.create(
#             order_number=data['order_data']['Order No:'],
#             order_placed_at=order_placed_at,
#             order_delivered_at=order_delivered_at,
#             order_status=data['order_data']['Order Status'],
#             restaurant=restaurant,
#             customer=customer,
#             order_total=data['order_summary']['Order Total']
#         )

#         # Create and save the Item objects
#         for item in data['item_details']:
#             if 'not found' in item[0].lower() or 'not found' in str(item[1]).lower() or 'not found' in str(item[2]).lower():
#                 continue
#             Item.objects.create(
#                 order=order,
#                 iname=item[0],
#                 quantity=item[1],
#                 price=item[2],
#                 itotal=item[1]*item[2]
#             )

#         # Create and save the Payment object
#         if 'not found' in str(data['order_summary']['Item Total']).lower() or \
#            'not found' in str(data['order_summary']['Order Packing Charges']).lower() or \
#            'not found' in str(data['order_summary']['Delivery partner fee']).lower() or \
#            'not found' in str(data['order_summary']['Discount Applied']).lower() or \
#            'not found' in str(data['order_summary']['Taxes']).lower():
#              #  'not found' in str(data['order_summary']['Platform fee']).lower() or \
#             continue
#         Payment.objects.create(
#             order=order,
#             payment_method='Unknown',  # Update this as per your data
#             items_total=data['order_summary']['Item Total'],
#             packing_charges=data['order_summary']['Order Packing Charges'],
#             platform_fee=data['order_summary']['Platform fee'],
#             delivery_partner_fee=data['order_summary']['Delivery partner fee'],
#             discount_applied=data['order_summary']['Discount Applied'],
#             taxes=data['order_summary']['Taxes'],
#             order_total=data['order_summary']['Order Total']
#         )

#     return HttpResponse("Data successfully added")



def successfully_scrap(request):
    received_data = getEmails(request)  # received_data contains the list with data
    print(received_data)

    for data in received_data:
        # Check if any field contains 'not found'
        if 'not found' in data['restaurant']['restaurant_name'].lower() or \
           'not found' in data['restaurant']['restaurant_address'].lower() or \
           'not found' in data['customer_info']['customer_name'].lower() or \
           'not found' in data['customer_info']['customer_address'].lower() or \
           'not found' in data['order_data']['Order No:'].lower() or \
           'not found' in data['order_data']['Order placed at:'].lower() or \
           'not found' in data['order_data']['Order delivered at:'].lower() or \
           'not found' in data['order_data']['Order Status'].lower() or \
           'not found' in str(data['order_summary']['Order Total']).lower():
            continue

        # Check if the Customer object exists, if not create a new one
        customer, created = Customer.objects.get_or_create(
            user = request.user,
            cname=data['customer_info']['customer_name'],
            caddress=data['customer_info']['customer_address']
        )
        print('customer created', created)
        
        # Create and save the Restaurant object
        restaurant, created = Restaurant.objects.get_or_create(
            rname=data['restaurant']['restaurant_name'],
            raddress=data['restaurant']['restaurant_address']
        )
        print('restaurant created',created)
        # Create and save the Order object
        order_placed_at = datetime.strptime(data['order_data']['Order placed at:'], '%A, %B %d, %Y %I:%M %p').replace(tzinfo=pytz.UTC) if 'not found' not in data['order_data']['Order placed at:'].lower() else None
        order_delivered_at = datetime.strptime(data['order_data']['Order delivered at:'], '%A, %B %d, %Y %I:%M %p').replace(tzinfo=pytz.UTC) if 'not found' not in data['order_data']['Order delivered at:'].lower() else None

        try: 
            order , order_created = Order.objects.get_or_create(
            restaurant = restaurant,
            order_number=data['order_data']['Order No:'],
            order_placed_at=order_placed_at,
            order_delivered_at=order_delivered_at,
            order_status=data['order_data']['Order Status'],
            customer=customer,
            order_total=data['order_summary']['Order Total']
        )
        
        except IntegrityError as e:
            print("errorr as ",e)
            continue

        for item in data['item_details']:
            if 'not found' in item[0].lower() or 'not found' in str(item[1]).lower() or 'not found' in str(item[2]).lower():
                continue
            Item.objects.create(
                order=order,
                iname=item[0],
                quantity=item[1],
                price=item[2]
            )

        # Create and save the Payment object
        # if 'not found' in str(data['order_summary']['Item Total']).lower() or \
        #    'not found' in str(data['order_summary']['Order Packing Charges']).lower() or \
        #    'not found' in str(data['order_summary']['Delivery partner fee']).lower() or \
        #    'not found' in str(data['order_summary']['Discount Applied']).lower() or \
        #    'not found' in str(data['order_summary']['Taxes']).lower():
        #     continue
        Payment.objects.create(
            order=order,
            payment_method='Unknown',  # Update this as per your data
            items_total=data['order_summary']['Item Total'],
            packing_charges=data['order_summary']['Order Packing Charges'],
            platform_fee=data['order_summary']['Platform fee'],
            delivery_partner_fee=data['order_summary']['Delivery partner fee'],
            discount_applied=data['order_summary']['Discount Applied'],
            taxes=data['order_summary']['Taxes'],
            order_total=data['order_summary']['Order Total']
        )

    return HttpResponse('Data Added Successfully')

def chart_data2(request):
    # Query the database for the necessary data
    try:
        chart_data = {
            # 'chart_1': {'orders_by_status_data': orders_by_status()},
            # 'chart_2' : {'quantity_by_item_data':quantity_by_item()},
            'chart_3' : {'orders_over_time':orders_over_time()}
        }
        print('chart_data----->',chart_data.get('chart_3'))
        return render(request, 'app/order_chart2.html', {'chart_data': chart_data})
    except Exception as e:
        # Handle exceptions gracefully
        error_message = f"An error occurred: {str(e)}"
        return HttpResponse(error_message)

def change_password(request):
 return render(request, 'app/changepassword.html')
    
class CustomerRegistrationView(View):
 def get(self,request):
  form = CustomerRegistrationForm()
  return render(request,'app/customerregistration.html',{'form':form})
 def post(self,request):
  form = CustomerRegistrationForm(request.POST)
  if form.is_valid():
   form.save()
   messages.success(request,'Congratulations! Registration Successfully')
   return redirect(reverse('login'))
  return render(request,'app/customerregistration.html',{'form':form})
 
def readytoscrap(request):
    if request.user.is_authenticated:
        return render(request,'app/readytoscrap.html')
    else:
        messages.warning(request,'Login to access scrapping functionality')
        return redirect(reverse('login'))
    
def home(request):
    if request.user.is_authenticated:
        return redirect(reverse('readytoscrap'))
    else:
        return render(request,'app/home.html')
