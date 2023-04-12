from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import vendingMachine, stock, time
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json


## create a vending machine with name and location. This will work with both Json and form-data input
## where it will check if the vending machine already exists, so it will stop duplicates.
@csrf_exempt
def create_vendingMachine(request):
    if request.method == 'POST':
        # checks if it's a json
        if request.content_type == "application/json":
            json_data = json.loads(request.body)
            name = json_data.get('name')
            location = json_data.get('location')
            
        else:
            name = request.POST.get('name')
            location = request.POST.get('location')
        
        # Checks if the name already exists.
        if vendingMachine.objects.filter(name=name).exists():
            return JsonResponse({'message': 'Vending Machine already exists.'})
            
        new_vm = vendingMachine(name=name, location=location)
        new_vm.save()
        time.objects.create(container=new_vm, key=timezone.now())
        print(vendingMachine.objects.filter(name='vending machine 1').exists())
        return JsonResponse({'message': f'Vending Machine {new_vm.id}, {new_vm.name} at {new_vm.location} is created.'})


## Edit a vending machine with the specified id where it will check if the vending machine exists.
## Can either change the name or location.
@csrf_exempt
def edit_vendingMachine(request):
    # vm = get_object_or_404(vendingMachine, id=id)
    if request.method == 'POST':
        vm_id = request.POST.get('id')
        new_name = request.POST.get('new name', None)
        new_loc = request.POST.get('new location', None)

        try:
            vm = vendingMachine.objects.get(id=vm_id)
        except vendingMachine.DoesNotExist:
            return JsonResponse({'message': 'Vending machine does not exist.'})

        if new_name:
            vm.name = new_name
    
        if new_loc:
            vm.location = new_loc
        
        vm.save()

        return JsonResponse({'message': f'Vending Machine {vm_id} is edited.'})


## Delete a vending machine with specified id where it will check if it exists first.
@csrf_exempt
def delete_vendingMachine(request):
    vm_id = request.POST.get('id')

    try:
        vm = vendingMachine.objects.get(id=vm_id)
    except vendingMachine.DoesNotExist:
        return JsonResponse({'message': 'Vending machine does not exist.'})

    vm.delete()

    return JsonResponse({'message': f'Vending Machine {vm_id} has been succesfully deleted.'})


## List all the vending machines in the database.
@csrf_exempt
def list_vendingMachine(request):
    vm = vendingMachine.objects.all().values('id', 'name', 'location')
    return JsonResponse({'Vending Machines': list(vm)})


## Add an item, item amount and item price into a specified vending machine.
@csrf_exempt
def add_item(request):
    if request.method == 'POST':
        vm_id = request.POST.get('id')

        try:
            vm = vendingMachine.objects.get(id=vm_id)
        except vendingMachine.DoesNotExist:
            return JsonResponse({'message' : 'Vending machine does not exist.'})

        name = request.POST.get('name')
        amount = request.POST.get('amount')
        price = request.POST.get('price')
            
        ## Checks if the item is already in the vending machine.
        if stock.objects.filter(vm=vm, name=name).exists():
            return JsonResponse({'message' : f'Vending Machine {vm_id} already has this item listed.'})

        stock_timestamp = []
        for stocks in vm.stock_set.all():
            stock_timestamp.append({
                'id': stocks.id,
                'name': stocks.name,
                'price': stocks.price,
                'amount': stocks.amount
            })
        time.objects.create(container=vm, key=timezone.now(), item=stock_timestamp)

        new_item = stock.objects.create(vm=vm, name=name, amount=amount, price=price)

        return JsonResponse({'message' : f'{new_item.amount} {new_item.name} is added into vending machine {vm_id}.'})

## Edit the edit of the specified name and vending machine.
@csrf_exempt
def edit_item(request):
    if request.method == 'POST':
        vm_id = request.POST.get('id')

        try:
            vm = vendingMachine.objects.get(id=vm_id)
        except vendingMachine.DoesNotExist:
            return JsonResponse({'message' : 'Vending machine does not exist.'})

        name = request.POST.get('name')
        new_name = request.POST.get('new name', None)
        new_amount = request.POST.get('new amount', None)
        new_price = request.POST.get('new price', None)

        # Checks if the item exists in the vending machine.
        if not stock.objects.filter(vm=vm, name=name).exists():
            return JsonResponse({'message': f'Item does not exist in vending machine {vm_id}'})
            
        stock_timestamp = []
        for stocks in vm.stock_set.all():
            stock_timestamp.append({
                'id': stocks.id,
                'name': stocks.name,
                'price': stocks.price,
                'amount': stocks.amount
            })
        time.objects.create(container=vm, key=timezone.now(), item=stock_timestamp)

        item = stock.objects.get(vm=vm, name=name)

        if new_name:
            item.name = new_name
        if new_amount:
            item.amount = new_amount
        if new_price:
            item.price = new_price
        item.save()

        return JsonResponse({'message' : f'The item in vending machine {vm_id} is updated.'})

## Delete the item from the specified vending machine.
@csrf_exempt
def delete_item(request):
    if request.method == 'POST':
        vm_id = request.POST.get('id')

        # checks if the vending machine exists
        try:
            vm = vendingMachine.objects.get(id=vm_id)
        except vendingMachine.DoesNotExist:
            return JsonResponse({'message' : 'Vending machine does not exist.'})

        name = request.POST.get('name')
        # checks if the item exisits in the vending machine
        if not stock.objects.filter(vm=vm, name=name).exists():
            return JsonResponse({'message' : 'The item does not exists in the vending machine.'})

        stock_timestamp = []
        for stocks in vm.stock_set.all():
            stock_timestamp.append({
                'id': stocks.id,
                'name': stocks.name,
                'price': stocks.price,
                'amount': stocks.amount
            })
        time.objects.create(container=vm, key=timezone.now(), item=stock_timestamp)
        
        item = stock.objects.get(vm=vm, name=name)
        item.delete()

        return JsonResponse({'message' : f'{name} in vending machine {vm_id} has been successfully removed.'})
    

## Lists all items in the specified vending machine.
@csrf_exempt
def list_items(request):
    if request.method == 'POST':
        vm_id = request.POST.get('id')

        try:
            vm = vendingMachine.objects.get(id=vm_id)
        except vendingMachine.DoesNotExist:
            return JsonResponse({'message' : 'Vending machine does not exist.'})

        items = stock.objects.filter(vm=vm).all()
        item_list = []

        for i in items:
            item_list.append({'name': i.name, 'amount': i.amount, 'price': i.price})
        
        # When the vending machine is empty.
        if len(item_list) == 0:
            return JsonResponse({'message' : f'Vending machine {vm_id} is empty.'})

        return JsonResponse({f'items in vending machine {vm_id}' : item_list})
        


@csrf_exempt
def list_time(request):
    if request.method == 'POST':
        vm_id = request.POST.get('id')
        if vendingMachine.objects.filter(id=vm_id).exists():
            vm = vendingMachine.objects.get(id=vm_id)
            times = time.objects.filter(container=vm).all()
            time_list = []

            for i in times:
                time_list.append({'time': i.key, 'items': i.item})

            return JsonResponse({f'time stamp in vending machine {vm_id}': time_list})
        else:
            return JsonResponse({'message': 'The vending machine does not exists.'})