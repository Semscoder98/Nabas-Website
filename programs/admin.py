from django.contrib import admin
from django.db import models
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Program, Scholarship, Resource, EventRegistration

class EventRegistrationInline(admin.TabularInline):
    model = EventRegistration
    extra = 0
    readonly_fields = ('registered_at',)


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'venue', 'category', 'is_upcoming', 'order')
    list_filter = ('is_upcoming', 'category')
    search_fields = ('title', 'theme', 'venue', 'description')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_upcoming', 'order')
    inlines = [EventRegistrationInline]
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='extends')},
    }


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'program', 'institution', 'phone', 'email', 'registered_at')
    list_filter = ('program', 'registered_at')
    search_fields = ('full_name', 'institution', 'phone', 'email', 'program__title')
    readonly_fields = ('registered_at',)


@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ('title', 'donor_organization', 'award_amount', 'deadline', 'is_open')
    list_filter = ('is_open',)
    search_fields = ('title', 'donor_organization', 'description')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_open',)
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='extends')},
    }


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'file_size', 'downloads_count', 'uploaded_at')
    list_filter = ('category', 'uploaded_at')
    search_fields = ('title', 'description')
    readonly_fields = ('downloads_count',)
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='extends')},
    }
