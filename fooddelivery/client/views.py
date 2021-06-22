from django.shortcuts import render
from django.views import View
from .models import MenuItem, Category, OrderModel


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')
class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'about.html')

class Order(View):

    def get(self, request, *args, **kwargs):
        Fruites = MenuItem.objects.filter(category__name__contains='Fruits')
        chaussures = MenuItem.objects.filter(category__name__contains='Chaussure')
        vetements = MenuItem.objects.filter(category__name__contains='vetements')
        drinks = MenuItem.objects.filter(category__name__contains='Drink')

        context = {
            'Fruits': Fruites,
            'chaussures': chaussures,
            'vetements': vetements,
            'drinks': drinks,
        }
        return render(request, 'order.html', context)

    def post(self, request, *args, **kwargs):

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')
        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price,
            }
            order_items['items'].append(item_data)
        
        price = 0
        item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])
        
        order = OrderModel.objects.create(price=price)
        order.items.add(*item_ids)

        context = {
            'items': order_items['items'],
            'price': price
        }

        return render(request, 'order_confirmation.html', context)



class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        context = {
            'pk': order.pk,
            'items': order.items,
            'price': order.price
        }
        return render(request, 'order_confirmation.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        print(request.body)


class OrderPayConfirmation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'order_pay_confirmation.html')