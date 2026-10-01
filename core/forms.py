from django.forms import ModelForm, ValidationError
from core.models import Item
class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = [
            'title',
            'description',
            'location',
            'event_date',
            'category',
            'status'
        ]
        
    def clean_description(self):
        description = self.cleaned_data["description"]
        description.strip()
        if len(description) < 20:
            raise ValidationError(
                "توضیحات وارد شده نباید کمتر از 20 کاراکتر باشد."
            )
        return description
    
    def clean(self):
        clean_data = super().clean()
        event_date = clean_data["event_date"]
        status = clean_data["status"]
        location = clean_data["location"]
        title = clean_data["title"]
        if status == Item.Status.DELIVERED and event_date is None:
            raise ValidationError(
                "برای وضعیت تحویل داده شده تاریخ نمی‌تواند خالی باشد."
            )
            
        
        title.strip()
        if len(title) < 3 :
            raise ValidationError(
                "عنوان باید حداقل 3 کاراکتر داشته باشد."
            )
        
        location.strip()
        if len(location) < 3:
            raise ValidationError(
                "نام مکان مورد نظر کمتر از 3 کاراکتر نباید باشد."
            )
            
        return clean_data
        
        
    