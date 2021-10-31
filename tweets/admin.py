from django.contrib import admin
from django import forms

from tweets.models import Tag, Tweet


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    search_fields = ['title']


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ['user', 'content', 'created_at']
    search_fields = ['user__username', 'content']
    filter_horizontal = ['tags']

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == 'content':
            field.widget = forms.Textarea(attrs=field.widget.attrs)
        return field
