from datetime import date
import json
from django.core.exceptions import ValidationError

file_path1 = 'core/data/keywords.json'
file_path2 = 'core/data/bad_words.json'
file_path3 = 'core/data/university_loc.json'

class BusinuessRule:
    @staticmethod
    def event_date_condition(event_date):

        if event_date > date.today():
            raise ValidationError(
                "تاریخ ثبت نمی‌تواند در آینده باشد."
            )
        return event_date
        
    def title_check(title):
        
        with open(file_path1 , "r" , encoding="utf-8") as f1:
            data1 = json.load(f1)
            for i in data1["keywords"]:
                if title == i:
                    raise ValidationError(
                        "لطفا در عنوان جزئیات بیشتر را ذکر کنید."
                 )
        with open(file_path2, "r" , encoding="utf-8") as f2:
            data2 = json.load(f2)
            for i in data2["bad_words"]:
                if i in title :
                    raise ValidationError (
                        "از هرگونه ناسزا پرهیز کنید."
                    )
            return title
        
    def description_check(description):
        
        with open(file_path2, "r" , encoding="utf-8") as f2:
            data2 = json.load(f2)
            for i in data2["bad_words"]:
                if i in description :
                    raise ValidationError (
        "از هرگونه ناسزا پرهیز کنید."
                )     
            return description
        
    def location_check(location):
        
            with open(file_path3 , "r"  , encoding="utf-8") as f3:
                data3 = json.load(f3)
                for i in data3["valid_location"]:
                    if i not in location:
                        raise ValidationError(
                            "مکان مورد نظر نامعتبر است."
                        )
                return location