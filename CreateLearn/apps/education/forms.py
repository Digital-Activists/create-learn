from django import forms
from django.db.models import Q

from .models import Course


class SearchCourseForm(forms.ModelForm):
    def get_results(self):
        if not self.is_valid():
            return Course.objects.none()

        query = Q()

        for field_name, lookup in self.Meta.search_fields.items():
            value = self.cleaned_data.get(field_name)
            if value:
                query &= Q(**{lookup: value})

        return self.Meta.model.objects.filter(query)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name in self.Meta.search_fields.keys():
            self.fields[field_name].required = False

    class Meta:
        model = Course
        fields = ("title",)
        widgets = {
            "title": forms.TextInput(attrs={}),
        }
        search_fields = {
            "title": "title__icontains",
        }
