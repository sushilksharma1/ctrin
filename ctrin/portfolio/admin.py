from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Category, Project, ProjectImage, Service, TeamMember,
    Testimonial, BlogPost, ContactMessage, SiteSettings
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'project_count')
    prepopulated_fields = {'slug': ('name',)}
    
    def project_count(self, obj):
        return obj.projects.count()
    project_count.short_description = 'Projects'


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ('image', 'caption', 'order')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'project_date', 'is_featured', 'image_preview')
    list_filter = ('category', 'is_featured', 'project_date')
    search_fields = ('title', 'description', 'client_name')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'description', 'detailed_description')
        }),
        ('Images', {
            'fields': ('featured_image',)
        }),
        ('Project Details', {
            'fields': ('project_date', 'location', 'client_name', 'budget', 'duration')
        }),
        ('Settings', {
            'fields': ('is_featured',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" width="50" height="50" />', obj.featured_image.url)
        return "No Image"
    image_preview.short_description = 'Preview'


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'icon')
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'icon')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Details', {
            'fields': ('features', 'order')
        }),
    )


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'experience_years', 'image_preview', 'order')
    list_filter = ('position', 'experience_years')
    search_fields = ('name', 'position')
    list_editable = ('order',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'position', 'experience_years', 'specialization')
        }),
        ('Bio', {
            'fields': ('bio',)
        }),
        ('Contact', {
            'fields': ('email', 'phone')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Social Links', {
            'fields': ('social_links',),
            'classes': ('collapse',)
        }),
        ('Order', {
            'fields': ('order',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Photo'


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_company', 'rating_stars', 'is_featured', 'order')
    list_filter = ('rating', 'is_featured')
    search_fields = ('client_name', 'client_company', 'content')
    list_editable = ('is_featured', 'order')
    fieldsets = (
        ('Client Information', {
            'fields': ('client_name', 'client_position', 'client_company', 'client_image')
        }),
        ('Content', {
            'fields': ('content', 'rating')
        }),
        ('Settings', {
            'fields': ('is_featured', 'order')
        }),
    )
    
    def rating_stars(self, obj):
        return format_html('★' * obj.rating + '☆' * (5 - obj.rating))
    rating_stars.short_description = 'Rating'


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_published', 'created_at')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'content', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Post Information', {
            'fields': ('title', 'slug', 'author', 'featured_image')
        }),
        ('Content', {
            'fields': ('excerpt', 'content')
        }),
        ('Meta', {
            'fields': ('tags', 'is_published')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new post
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at', 'name', 'email', 'phone', 'subject', 'message', 'project_type', 'budget')
    
    def has_delete_permission(self, request):
        return False
    
    def has_add_permission(self, request):
        return False


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('General', {
            'fields': ('site_name', 'tagline', 'description', 'logo', 'favicon')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'address')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'instagram_url', 'twitter_url', 'linkedin_url'),
            'classes': ('collapse',)
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Footer', {
            'fields': ('footer_text',),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request):
        return False
