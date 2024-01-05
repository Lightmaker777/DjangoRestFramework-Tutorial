from typing import Any
from rest_framework import serializers
from .models import Book
from datetime import date
from rest_framework.exceptions import ValidationError
from django.utils.html import escape,strip_tags
from django.utils.text import slugify


class PastDateValidator:
    def __call__(self, value) :
        if value > date.today():
            raise ValidationError("Published date must be in the past.")

class UniqueTitleValidator:
    def __call__(self,value):
        if Book.objects.filter(title = value).exists():
            raise ValidationError("A book with this title already exists.")  
        
class CapitalizeName:
    def __call__(self, value) :
        return value.title()

class BookSerializer(serializers.ModelSerializer):
    published_date = serializers.DateField(required=True, validators=[PastDateValidator()])
    title = serializers.CharField( max_length = 200,required=True, validators=[UniqueTitleValidator()],trim_whitespace = True)
    author = serializers.CharField(max_length = 200,required=True,validators=[],trim_whitespace = True)
    description = serializers.CharField(required=False, allow_blank=True)
    
    def validate_title(self,value):
        return slugify(strip_tags(value))
    
    def validate_description(self,value):
        return strip_tags(value)
    
    def validate_author(self,value):
        return strip_tags(value)
    
    # def to_internal_value(self, data):
    #     # Sanitize is_published field by converting string value to boolean
    #     if 'is_published' in data:
    #         data['is_published'] = str(data['is_published']).lower() == 'true'
    #     return super().to_internal_value(data)
    
    def to_representation(self, instance):
        instance.author = CapitalizeName()(instance.author) #cap(instance.author)
        instance.title=CapitalizeName()(instance.title)
        return super().to_representation(instance)
        
    
    class Meta:
        model = Book
        #fields = '__all__'
        fields = ['id','title','author','description','published_date','is_published']