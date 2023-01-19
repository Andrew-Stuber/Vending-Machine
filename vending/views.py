from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import vendingMachine, stock
from django.views.decorators.csrf import csrf_exempt
import json

## create a vending machine with name and location. This will work with both Json and form-data input
## where it will check if the vending machine already exists, so it will stop duplicates.
@csrf_exempt
def create_vendingMachine(request):
    if request.method == 'POST':
        if request.content_type == "application/json":
            json_data = json.loads(request.body)
            name = json_data.get('name')
            location = json_data.get('location')
            if vendingMachine.objects.filter(name=name).exists():
                return JsonResponse({'message': 'Vending Machine already exists.'})
        else:
            name = request.POST.get('name')
            location = request.POST.get('location')
            if vendingMachine.objects.filter(name=name).exists():
                return JsonResponse({'message': 'Vending Machine already exists.'})
            
        new_vm = vendingMachine(name=name, location=location)
        new_vm.save()
        print(vendingMachine.objects.filter(name='vending machine 1').exists())
        return JsonResponse({'message': f'Vending Machine {new_vm.name} at {new_vm.location} is created.'})

## Edit a vending machine with the specified id where it will check if the vending machine exists.
## Can either change the name or location.
@csrf_exempt
def edit_vendingMachine(request):
    #vm = get_object_or_404(vendingMachine, id=id)
    if request.method == 'POST':
        vm_id = request.POST.get('id')
        new_name = request.POST.get('new name', None)
        new_loc = request.POST.get('new location', None)

        if vendingMachine.objects.filter(id=vm_id).exists():
            vm = vendingMachine.objects.get(id=vm_id)

            if new_name:
                vm.name = new_name
    
            if new_loc:
                vm.location = new_loc
        
            vm.save()

            return JsonResponse({'message': f'Vending Machine {vm_id} is edited.'})
        else:
            return JsonResponse({'message': f'Vending machine does not exists.'})

## Delete a vending machine with specified id where it will check if it exists first.
@csrf_exempt
def delete_vendingMachine(request):
    vm_id = request.POST.get('id')
    if vendingMachine.objects.filter(id=vm_id).exists():
        vm = vendingMachine.objects.get(id=vm_id)
        vm.delete()
        return JsonResponse({'message': f'Vending Machine {vm_id} has been succesfully deleted.'})
    else:
        return JsonResponse({'message': 'Vending Machine does not exsits.'})

