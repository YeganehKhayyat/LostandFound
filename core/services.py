from datetime import date
import json
from django.core.exceptions import ValidationError

file_path = 'core/data/keywords.json'

class BusinuessRule:
    @staticmethod
    def event_date_condition(event_date):

        if event_date > date.today():
            raise ValidationError(
                "تاریخ ثبت نمی‌تواند در آینده باشد."
            )
        return event_date
        
    def title_check(title):
        
        with open(file_path , "r" , encoding="utf-8") as f:
            data = json.load(f)
            for i in data["keywords"]:
                if title == i:
                    raise ValidationError(
                        "لطفا در عنوان جزئیات بیشتر را ذکر کنید."
                 )
            return title
        