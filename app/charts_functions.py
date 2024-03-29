# from .models import Restaurant, Customer, Order, Item, Payment
# from django.db.models import Count, Sum
# from django.db.models.functions import TruncDay


# def orders_by_status():
#     orders_by_status = Order.objects.values('order_status').annotate(count=Count('id'))
#     orders_by_status_dict = {item['order_status']: item['count'] for item in orders_by_status}
#     return orders_by_status_dict

# def quantity_by_item():
#     quantity_by_item = Item.objects.values('iname').annotate(quantity=Sum('quantity'))
#     quantity_by_item_dict = {item['iname']: item['quantity'] for item in quantity_by_item}
#     return (quantity_by_item_dict)

# def orders_over_time():
#         # import library TruncDay
#         data = Order.objects.annotate(date=TruncDay('order_placed_at')).values('date').annotate(c=Count('id')).values('date', 'c')
#         # print(data)
#         return list(data)

# from django.contrib.auth.decorators import login_required

# @login_required
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.db.models.functions import TruncDay
from .models import Restaurant, Customer, Order, Item, Payment

@login_required
def orders_by_status(request):
    orders_by_status = Order.objects.filter(customer__user=request.user).values('order_status').annotate(count=Count('id'))
    orders_by_status_dict = {item['order_status']: item['count'] for item in orders_by_status}
    print(orders_by_status_dict)
    return orders_by_status_dict 

@login_required
def quantity_by_item(request):
    orders = Order.objects.filter(customer__user=request.user)
    quantity_by_item = Item.objects.filter(order__in=orders).values('iname').annotate(quantity=Sum('quantity'))
    quantity_by_item_dict = {item['iname']: item['quantity'] for item in quantity_by_item}
    print(quantity_by_item_dict)
    return quantity_by_item_dict

@login_required
def orders_over_time(request):
    data = Order.objects.filter(customer__user=request.user).annotate(date=TruncDay('order_placed_at')).values('date').annotate(c=Count('id')).values('date', 'c')
    print(data)
    return list(data)

