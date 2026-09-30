from django.shortcuts import render
from core.forms import ItemForm

# Create your views here.

def create_item(requests):
    
    if requests.method == "POST":
        
        # title = '1100', description = 'i found it', ...
        form = ItemForm(requests.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = requests.user
            item.save()
            return render(
                    requests, 
                    "items/create.html" ,
                    context= {'form' : form}
                    )
            
        else:
            ...
            
    else:
        form = ItemForm()
        
    return render(
        requests, 
        "items/create.html" ,
        context= {'form' : form}
        )