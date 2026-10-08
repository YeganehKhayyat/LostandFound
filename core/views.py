from django.shortcuts import render, redirect ,get_object_or_404
from core.forms import ItemForm
from core.models import Item
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db import models
from django.contrib import messages
from django.db.models import Q
# Create your views here.

def list_items(requests):
    '''
    SELECT * 
    FROM TABLE_NAME
    '''
    
    items = Item.objects.all().order_by("-created_at").values()
    query = requests.GET.get("q")
    status = requests.GET.get("status")
    category = requests.GET.get("category")
    # selected_date = requests.GET.get("created_at")
    start_date = requests.GET.get("start_date")
    end_date = requests.GET.get("end_date")
    
    # if selected_date:
    #     items = items.filter(created_at__date= selected_date)
        
    if start_date:
        items = items.filter(created_at__gte=start_date)
        
    if end_date:
        items = items.filter(created_at__date = end_date)
    
    if query:
        items = items.filter(
            Q(title__icontains= query) |
            Q(location__icontains = query) |
            Q(description__icontains = query)
        )
    
    if status :
        items = items.filter(
            status = status
        )
        
    if category:
        items = items.filter(
            category_id = category
        )
        
    print(items.query)
    
    return render(
        requests,
        "items/item_list.html",
        context={
            'items' : items ,
            'start_date' : start_date,
            'end_date' : end_date
            }
    )

@login_required(login_url='/admin')
def create_item(requests):
    
    if requests.method == "POST":
        
        # title = '1100', description = 'i found it', ...
        form = ItemForm(
            requests.POST,
            requests.FILES
            )
        
        print(requests.POST)
        print(requests.FILES)
        
        if form.is_valid():
            
            item = form.save(commit=False)
            item.created_by = requests.user
            item.save()
            messages.success(
                requests,
                f"آیتم {item.title} با موفقیت ایجاد شد."
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
    
@login_required(login_url='/admin')  
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
    
@login_required(login_url='/admin')
def update_item(requests, pk):
    item  = get_object_or_404(
                Item,
                id = pk,
                created_by = requests.user
            )

    if requests.method == "POST":
         print("Files received:", requests.FILES)
         form = ItemForm(
             requests.POST,
             requests.FILES,
             instance=item
             )
         
         if form.is_valid():
            form.save()
            messages.success(
                 requests,
                 f"آیتم {item.title} با موفقیت ویرایش شد."
             )
             
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

@login_required(login_url='/admin')
def delete_item(requests, pk):
    item  = get_object_or_404(
                    Item,
                    id = pk,
                    created_by = requests.user
                ) 
    
    if requests.method == "POST":
        item_title = item.title
        item.delete()
        messages.success(
        requests, 
        f"آیتم {item_title} با موفقیت حذف شد."
        )
        
        return redirect('report')

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