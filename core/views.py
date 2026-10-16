from django.shortcuts import render, redirect ,get_object_or_404
from core.forms import ItemForm, ClaimForm
from core.models import Item, Claim
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db import models
from django.contrib import messages
from django.db.models import Q
from core.workflows import can_transition, can_create_claim
# Create your views here.

def list_items(requests):
    '''
    SELECT * 
    FROM TABLE_NAME
    '''
    
    items = Item.objects.all()
    
    query = requests.GET.get("q")
    
    status = requests.GET.get("status")
    
    category = requests.GET.get("category")

    start_date = requests.GET.get("start_date")
    end_date = requests.GET.get("end_date")
    
    
    
    if start_date:
        items = items.filter(created_at__date__gte=start_date)
        
    if end_date:
        items = items.filter(created_at__date__lte = end_date)
    
    sort_val = requests.GET.get("sort")
    
    sort_options = {
            "newest" : "-created_at",
            "oldest" : "created_at"
        }
    
    if sort_val:
            
        sort_field = sort_options.get(sort_val , "-created_at")
        items = items.order_by(sort_field)
    
    if query:
        items = items.filter(
            Q(title__contains= query) |
            Q(location__contains = query) |
            Q(description__contains = query)
        )
    
    if status :
        items = items.filter(
            status = status
        )
        
    if category:
        items = items.filter(
            category_id = category
        )
        
    result_num = items.count()
    
    return render(
        requests,
        "items/item_list.html",
        context={
            'items' : items ,
            'start_date' : start_date,
            'end_date' : end_date,
            'sort' : sort_val,
            'result_num' : result_num
            }
    )

@login_required(login_url='/login')
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
    
@login_required(login_url='/login')  
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
    
@login_required(login_url='/login')
def update_item(requests, pk):
    print(requests.user.get_all_permissions("core.change_item"))
    item  = get_object_or_404(
                Item,
                id = pk,
                created_by = requests.user
            )
      
    if requests.method == "POST":
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

@login_required(login_url='/login')
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
    
@login_required(login_url='/login')
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
    
@login_required(login_url='/login')
def change_status(requests, pk):
    
    new_status = requests.POST.get("status")
    
    item  = get_object_or_404(
                Item,
                id = pk,
                created_by = requests.user
            )
    
    # Guard clause
    if not can_transition(item , new_status): 
        messages.error(
            requests,
        "این تغییر وضعیت ممکن نیست."
        )
        return redirect( 
        "item_detail" ,
        pk = item.id
    )
        
    item.status = new_status
    item.save()
        
    messages.success(
            requests,
            f"ایتم به وضعیت {new_status} "
        )
    return redirect(
        "item_detail",
        pk = item.id
    )

@login_required(login_url='/login')    
def submit_claim(requests , pk):
    # Form
    # Validation
    
    item  = get_object_or_404(
        Item,
        id = pk
    )
    # form validation
    if not can_create_claim(item, requests.user):
        messages.error(
            requests,
            f"ثبت درخواست برای این آیتم امکان پذیر نیست."
        )
        return redirect(
            "item_detail",
            pk = item.id
        )
        
    if requests.method == "POST":
        form = ClaimForm(requests.POST)
        
        if form.is_valid():
            claim = form.save(commit=False)
            
            claim.item = item
            claim.claimant = requests.user
            claim.status = Claim.Status.PENDING
            claim.save()
            
            messages.success(
                requests , 
                "مالکیت شما ثبت شد"
            )
            return redirect(
                "item_detail" ,
                pk = item.id
            )
    else:
        form = ClaimForm()
        
    return render(
        requests , 
        "items/submit_claim.html" , 
        context= 
        {
            'form' : form,
            'item' : item
            }
    )
    
@login_required(login_url="/login")
def claim_review_list(requests):
    claims = Claim.objects.filter(
        status = Claim.Status.PENDING
    ).order_by("-created_at")
    
    return render (
        requests,
        "claim/review_list.html",
        {'claims' : claims}
    )
    
@login_required(login_url="/login")    
def approve_reject_claim(requests, pk):
    claim = get_object_or_404(
        Claim,
        id=pk
    )
    if requests.method == "POST":
        new_status = requests.POST.get("status")
        
        if new_status == 'approve':
            claim.status = Claim.Status.APPROVED
            claim.item.status = Item.Status.REVIEWING
            claim.item.save()
            claim.save()
            msg_txt = "درخواست مالکیت تایید شد"
            
        elif new_status == 'reject':
            claim.status = Claim.Status.REJECTED
            claim.save()
            msg_txt = "درخواست مالکیت رد شد"
            
            
        else:
            msg_txt = "درخواست مالکیت وضعیت درستی ندارد"
        
        messages.success(
            requests ,
            msg_txt
        )
    
    return redirect(
        "claim_review_list"
        )