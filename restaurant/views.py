# restaurant/views.py
from django.shortcuts import render
import random
from datetime import datetime, timedelta
import time

# View for the main page
def main(request):
    return render(request, 'restaurant/main.html')


# View for the order page
def order(request):
    specials = ['Pizza', 'Burger', 'French Fries', 'Hot Dog']
    daily_special = random.choice(specials)
    context = {
        'daily_special': daily_special
    }
    return render(request, 'restaurant/order.html', context)

# View for the confirmation page
def confirmation(request):
    if request.method == 'POST':
        # Collect form data
        customer_name = request.POST.get('name')
        customer_phone = request.POST.get('phone')
        customer_email = request.POST.get('email')
        ordered_items = request.POST.getlist('items')
        pizza_toppings = request.POST.getlist('toppings') if 'Pizza' in ordered_items else []
        special_instructions = request.POST.get('instructions')

        # Define item prices
        menu_prices = {
            'Pizza': 10,
            'Burger': 8,
            'French Fries': 12,
            'Hot Dog': 15,
        }

        # Calculate total price
        total_price = sum(menu_prices[item] for item in ordered_items if item in menu_prices)

        # Calculate ready time (randomly between 30 and 60 minutes from now)
        ready_time = datetime.now() + timedelta(minutes=random.randint(30, 60))

        # Prepare context for confirmation page
        context = {
            'customer_name': customer_name,
            'customer_phone': customer_phone,
            'customer_email': customer_email,
            'ordered_items': ordered_items,
            'pizza_toppings': pizza_toppings,
            'special_instructions': special_instructions,
            'total_price': total_price,
            'ready_time': ready_time.strftime('%H:%M'),
            "current_time" : time.ctime()
        }


    

        return render(request, 'restaurant/confirmation.html', context)