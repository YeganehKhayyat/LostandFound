from django.shortcuts import render, redirect ,get_object_or_404
from core.forms import ItemForm
from core.models import Item
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db import models
from django.contrib import messages
from django.urls import reverse
# Create your views here.

def list_items(requests):
    '''
    SELECT * 
    FROM TABLE_NAME
    '''
    
    items = Item.objects.all()
    return render(
        requests,
        "items/item_list.html",
        context={'items' : items}
    )

def create_item(requests):
    
    if requests.method == "POST":
        
        # title = '1100', description = 'i found it', ...
        form = ItemForm(requests.POST)
        if form.is_valid():
            
            item = form.save(commit=False)
            item.created_by = requests.user
            item.save()
            messages.success(
                requests,
                "آیتم با موفقیت ایجاد شد."
            )
            
            return redirect(
                'item_detail',
                pk=item.id
            )
            
        else:
            print(form.errors)
            # print("*"  * 10)
            # print(form.non_field_errors)
            
    else:
        form = ItemForm()
        
    return render(
        requests, 
        "items/create.html" ,
        context= {'form' : form}
        )
    
@login_required    
def item_detail(requests, pk):

    item = get_object_or_404(
        Item,
        id=pk
        )
    
    return render(
        requests,
        "items/item_detail.html",
        {'item' : item}
    )
    
@login_required
def update_item(requests, pk):
    item  = get_object_or_404(
                Item,
                id = pk,
                created_by = requests.user
            ) 
    
    if requests.method == "POST":
         form = ItemForm(
             requests.POST,
             instance=item
             )
         
         if form.is_valid():
             form.save()
             return redirect(
                            "item_detail",
                             pk=item.id
                             )
             
    else:
        
        form = ItemForm(instance=item)
        
    return render(
        requests, 
        "items/update.html" ,
        context= {'form' : form}
        )

@login_required  
def delete_item(requests, pk):
    item  = get_object_or_404(
                    Item,
                    id = pk,
                    created_by = requests.user
                ) 
    
    if requests.method == "POST":
        item.delete()
        return redirect('list_item')
    
    return render(
        requests,
        "items/confirm_delete.html",
        {'item' : item}
    )
    
@login_required(login_url='/admin')
def report(requests):
    
    item = Item.objects.filter(
        created_by = requests.user
    ).order_by('-event_date')
    
    state = item.aggregate(
        opened = Count('id' , filter=models.Q(status='open')),
        closed = Count('id' , filter=models.Q(status = 'closed'))
    )
    return render(
        requests,
        "items/report.html",
        {
         'item' : item,
         'state' : state
         }
    )