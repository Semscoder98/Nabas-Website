from django.contrib import admin
from django.db import models
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import (
    ContactMessage,
    ExecutiveMember,
    ExecutiveCouncilMember,
    ParliamentaryCouncilMember,
    DirectorateMember,
    AdvisoryCouncilMember,
    PastLeader,
    GalleryImage,
    Donation,
    Partner,
)

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'order', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name',)
    list_editable = ('order', 'is_active')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)


from django import forms

# Base Leadership Admin configuration with targeted rich-text support
class BaseCouncilAdmin(admin.ModelAdmin):
    list_per_page = 25

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'quote':
            kwargs['widget'] = forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Personal quote, motto, or short citation (plain text, no HTML tags)'
            })
        elif db_field.name == 'responsibilities':
            kwargs['widget'] = forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Key portfolio duties / statutory responsibilities (one per line)'
            })
        elif db_field.name == 'bio':
            kwargs['widget'] = CKEditor5Widget(config_name='extends')
        return super().formfield_for_dbfield(db_field, request, **kwargs)


@admin.register(ExecutiveCouncilMember)
class ExecutiveCouncilMemberAdmin(BaseCouncilAdmin):
    list_display = ('name', 'role', 'tag', 'tenure', 'institution', 'is_spotlight', 'order')
    list_filter = ('is_spotlight', 'tenure')
    search_fields = ('name', 'role', 'tag', 'institution', 'bio', 'quote')
    list_editable = ('order', 'is_spotlight')
    actions = ['move_to_past_leaders', 'toggle_spotlight']
    fieldsets = (
        ('Executive Officer Information', {
            'fields': ('name', 'role', 'tag', 'tenure', 'institution', 'order')
        }),
        ('Tenure & Spotlight Controls', {
            'fields': ('is_spotlight', 'is_past_leader'),
            'description': 'Mark "is_spotlight" for the President to display on the featured executive spotlight banner. Check "is_past_leader" to retire this officer into the Past Leaders (Hall of Fame) at the end of their 1-year administration.'
        }),
        ('Media & Portrait', {
            'fields': ('image', 'image_url')
        }),
        ('Biography & Official Citation', {
            'fields': ('quote', 'bio', 'responsibilities')
        }),
        ('Contact & Social Media Links', {
            'fields': ('email', 'phone', 'linkedin_url', 'twitter_url', 'facebook_url'),
            'description': 'Direct channels for students to reach this executive officer.'
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(portfolio='exec', is_past_leader=False)

    def save_model(self, request, obj, form, change):
        if obj.is_past_leader:
            obj.portfolio = 'past'
            obj.is_spotlight = False
        else:
            obj.portfolio = 'exec'
        super().save_model(request, obj, form, change)

    @admin.action(description="Move selected to Past Leaders (End of 1-Year Tenure)")
    def move_to_past_leaders(self, request, queryset):
        updated = queryset.update(portfolio='past', is_past_leader=True, is_spotlight=False)
        self.message_user(request, f"Successfully moved {updated} executive officer(s) to Past Leaders / Hall of Fame.")

    @admin.action(description="Toggle Spotlight (President Featured Banner)")
    def toggle_spotlight(self, request, queryset):
        for leader in queryset:
            leader.is_spotlight = not leader.is_spotlight
            leader.save()
        self.message_user(request, f"Toggled spotlight for {queryset.count()} executive officer(s).")


@admin.register(ParliamentaryCouncilMember)
class ParliamentaryCouncilMemberAdmin(BaseCouncilAdmin):
    list_display = ('name', 'role', 'tag', 'tenure', 'institution', 'is_spotlight', 'order')
    list_filter = ('is_spotlight', 'tenure')
    search_fields = ('name', 'role', 'tag', 'institution', 'bio', 'quote')
    list_editable = ('order', 'is_spotlight')
    actions = ['move_to_past_leaders', 'toggle_spotlight']
    fieldsets = (
        ('Parliamentarian Information', {
            'fields': ('name', 'role', 'tag', 'tenure', 'institution', 'order')
        }),
        ('Tenure & Spotlight Controls', {
            'fields': ('is_spotlight', 'is_past_leader'),
            'description': 'Mark "is_spotlight" for the Rt. Hon. Speaker to display on the legislative spotlight banner. Check "is_past_leader" to move this parliamentarian to Past Leaders at tenure end.'
        }),
        ('Media & Portrait', {
            'fields': ('image', 'image_url')
        }),
        ('Biography & Chamber Citation', {
            'fields': ('quote', 'bio', 'responsibilities')
        }),
        ('Contact & Social Media Links', {
            'fields': ('email', 'phone', 'linkedin_url', 'twitter_url', 'facebook_url'),
            'description': 'Direct channels for constituency contact.'
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(portfolio='leg', is_past_leader=False)

    def save_model(self, request, obj, form, change):
        if obj.is_past_leader:
            obj.portfolio = 'past'
            obj.is_spotlight = False
        else:
            obj.portfolio = 'leg'
        super().save_model(request, obj, form, change)

    @admin.action(description="Move selected to Past Leaders (End of 1-Year Tenure)")
    def move_to_past_leaders(self, request, queryset):
        updated = queryset.update(portfolio='past', is_past_leader=True, is_spotlight=False)
        self.message_user(request, f"Successfully moved {updated} parliamentarian(s) to Past Leaders / Hall of Fame.")

    @admin.action(description="Toggle Spotlight (Speaker Featured Banner)")
    def toggle_spotlight(self, request, queryset):
        for leader in queryset:
            leader.is_spotlight = not leader.is_spotlight
            leader.save()
        self.message_user(request, f"Toggled spotlight for {queryset.count()} parliamentarian(s).")


@admin.register(DirectorateMember)
class DirectorateMemberAdmin(BaseCouncilAdmin):
    list_display = ('name', 'role', 'tag', 'tenure', 'institution', 'is_spotlight', 'order')
    list_filter = ('is_spotlight', 'tenure')
    search_fields = ('name', 'role', 'tag', 'institution', 'bio', 'quote')
    list_editable = ('order', 'is_spotlight')
    actions = ['move_to_past_leaders', 'toggle_spotlight']
    fieldsets = (
        ('Directorate / Appointee Information', {
            'fields': ('name', 'role', 'tag', 'tenure', 'institution', 'order'),
            'description': 'Use "Role" for their appointed office (e.g. Director of ICT & Innovation, Liaison Officer) and "Institution" for the institution or organization they represent.'
        }),
        ('Tenure & Spotlight Controls', {
            'fields': ('is_spotlight', 'is_past_leader'),
            'description': 'Mark "is_spotlight" to feature the Head of Directorates / Chief of Staff on the spotlight banner. Check "is_past_leader" to move this appointee to Past Leaders at tenure end.'
        }),
        ('Media & Portrait', {
            'fields': ('image', 'image_url')
        }),
        ('Biography & Mandate Citation', {
            'fields': ('quote', 'bio', 'responsibilities')
        }),
        ('Contact & Social Media Links', {
            'fields': ('email', 'phone', 'linkedin_url', 'twitter_url', 'facebook_url'),
            'description': 'Direct channels for students and institutions to reach this directorate officer.'
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(portfolio='directorate', is_past_leader=False)

    def save_model(self, request, obj, form, change):
        if obj.is_past_leader:
            obj.portfolio = 'past'
            obj.is_spotlight = False
        else:
            obj.portfolio = 'directorate'
        super().save_model(request, obj, form, change)

    @admin.action(description="Move selected to Past Leaders (End of 1-Year Tenure)")
    def move_to_past_leaders(self, request, queryset):
        updated = queryset.update(portfolio='past', is_past_leader=True, is_spotlight=False)
        self.message_user(request, f"Successfully moved {updated} directorate officer(s) to Past Leaders / Hall of Fame.")

    @admin.action(description="Toggle Spotlight (Directorate Featured Banner)")
    def toggle_spotlight(self, request, queryset):
        for leader in queryset:
            leader.is_spotlight = not leader.is_spotlight
            leader.save()
        self.message_user(request, f"Toggled spotlight for {queryset.count()} directorate officer(s).")


@admin.register(AdvisoryCouncilMember)
class AdvisoryCouncilMemberAdmin(BaseCouncilAdmin):
    list_display = ('name', 'role', 'tag', 'tenure', 'institution', 'is_spotlight', 'order')
    list_filter = ('is_spotlight', 'tenure')
    search_fields = ('name', 'role', 'tag', 'institution', 'bio', 'quote')
    list_editable = ('order', 'is_spotlight')
    actions = ['move_to_past_leaders', 'toggle_spotlight']
    fieldsets = (
        ('Patron & Advisory Information', {
            'fields': ('name', 'role', 'tag', 'tenure', 'institution', 'order')
        }),
        ('Tenure & Spotlight Controls', {
            'fields': ('is_spotlight', 'is_past_leader'),
            'description': 'Mark "is_spotlight" for the Grand / Chief Patron to display in the featured banner.'
        }),
        ('Media & Portrait', {
            'fields': ('image', 'image_url')
        }),
        ('Biography & Citation', {
            'fields': ('quote', 'bio', 'responsibilities')
        }),
        ('Contact & Links', {
            'fields': ('email', 'phone', 'linkedin_url', 'twitter_url', 'facebook_url'),
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(portfolio='advisory', is_past_leader=False)

    def save_model(self, request, obj, form, change):
        if obj.is_past_leader:
            obj.portfolio = 'past'
            obj.is_spotlight = False
        else:
            obj.portfolio = 'advisory'
        super().save_model(request, obj, form, change)

    @admin.action(description="Move selected to Past Leaders / Patrons Emeritus")
    def move_to_past_leaders(self, request, queryset):
        updated = queryset.update(portfolio='past', is_past_leader=True, is_spotlight=False)
        self.message_user(request, f"Successfully moved {updated} patron(s) to Past Leaders.")

    @admin.action(description="Toggle Spotlight (Chief Patron Featured Banner)")
    def toggle_spotlight(self, request, queryset):
        for leader in queryset:
            leader.is_spotlight = not leader.is_spotlight
            leader.save()
        self.message_user(request, f"Toggled spotlight for {queryset.count()} patron(s).")


@admin.register(PastLeader)
class PastLeaderAdmin(BaseCouncilAdmin):
    list_display = ('name', 'role', 'tag', 'tenure', 'institution', 'order')
    list_filter = ('tenure',)
    search_fields = ('name', 'role', 'tag', 'institution', 'bio', 'quote')
    list_editable = ('order',)
    actions = ['restore_to_sec', 'restore_to_spc', 'restore_to_directorate', 'restore_to_advisory']
    fieldsets = (
        ('Past Leader Citation', {
            'fields': ('name', 'role', 'tag', 'tenure', 'institution', 'order')
        }),
        ('Media & Portrait', {
            'fields': ('image', 'image_url')
        }),
        ('Legacy Biography & Historic Quote', {
            'fields': ('quote', 'bio', 'responsibilities')
        }),
        ('Contact & Archival Links', {
            'fields': ('email', 'phone', 'linkedin_url', 'twitter_url', 'facebook_url'),
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(models.Q(portfolio='past') | models.Q(is_past_leader=True))

    def save_model(self, request, obj, form, change):
        obj.is_past_leader = True
        obj.portfolio = 'past'
        obj.is_spotlight = False
        super().save_model(request, obj, form, change)

    @admin.action(description="Restore selected to Active Executive Council (SEC)")
    def restore_to_sec(self, request, queryset):
        updated = queryset.update(portfolio='exec', is_past_leader=False)
        self.message_user(request, f"Successfully restored {updated} leader(s) to Active SEC.")

    @admin.action(description="Restore selected to Active Parliamentary Council (SPC)")
    def restore_to_spc(self, request, queryset):
        updated = queryset.update(portfolio='leg', is_past_leader=False)
        self.message_user(request, f"Successfully restored {updated} leader(s) to Active SPC.")

    @admin.action(description="Restore selected to Active Directorates")
    def restore_to_directorate(self, request, queryset):
        updated = queryset.update(portfolio='directorate', is_past_leader=False)
        self.message_user(request, f"Successfully restored {updated} leader(s) to Active Directorates.")

    @admin.action(description="Restore selected to Active Patrons & Advisory Council")
    def restore_to_advisory(self, request, queryset):
        updated = queryset.update(portfolio='advisory', is_past_leader=False)
        self.message_user(request, f"Successfully restored {updated} patron(s) to Active Advisory.")


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'caption')


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('donor_name', 'email', 'amount', 'purpose', 'status', 'created_at')
    list_filter = ('status', 'purpose', 'created_at')
    search_fields = ('donor_name', 'email', 'reference')
