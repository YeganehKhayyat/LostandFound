from django.forms import ModelForm, ValidationError
from .models import Item
from django import forms
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
        return title
    
    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get("status")
        description = cleaned_data.get("description")
        
        if status == "closed" and not description:
            raise forms.ValidationError("وقتی وضعیت بسته است، باید توضیحات بنویسید!")
        
        return cleaned_data
        
        
    