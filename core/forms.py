from django.forms import ModelForm, ValidationError
from .models import Item
from django import forms
from core.services import BusinuessRule
class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = [
            'title',
            'description',
            'location',
            'event_date',
            'category',
            'status',
            'image'
            ]
        
    def clean_description(self):
        description = self.cleaned_data.get("description")
        if len(description) < 20:
            raise forms.ValidationError(
                "توضیحات وارد شده نباید کمتر از 20 کاراکتر باشد."
            )
        return description
    
    def clean_title(self):
        title = self.cleaned_data.get("title")
        if len(title) < 3 :
            raise forms.ValidationError(
            "عنوان خیلی کوتاه است. باید همانند «کیف پول» بیش از 3 کاراکتر داشته باشد."
        )
        try:
            return BusinuessRule.title_check(title)
        except ValueError as e:
            raise ValidationError(str(e))
    
    def clean_event_date(self):
        event_date = self.cleaned_data.get('event_date')
        try:
            return BusinuessRule.event_date_condition(event_date)
        except ValueError as e:
            raise forms.ValidationError(str(e))
        
    def clean_location(self):
        location = self.cleaned_data.get('location')
        
        try:
            return BusinuessRule.description_check(location)
        except ValueError as e:
            return forms.ValidationError(str(e))
        
    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image:
            if image.size > 2*1024*1024:
                raise ValidationError(
                    "حداکثر حجم مجاز : 2MB"
                )
        return image
                
    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get("status")
        description = cleaned_data.get("description")
        
        if status == "closed" and not description:
            raise forms.ValidationError("وقتی وضعیت بسته است، باید توضیحات بنویسید!")
        
        return cleaned_data
        
        
    