from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Category(models.Model):
    """Project categories"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Project(models.Model):
    """Interior design projects showcase"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='projects')
    description = models.TextField()
    detailed_description = models.TextField(blank=True)
    featured_image = models.ImageField(upload_to='projects/')
    project_date = models.DateField()
    location = models.CharField(max_length=200, blank=True)
    client_name = models.CharField(max_length=200, blank=True)
    budget = models.CharField(max_length=100, blank=True, help_text="e.g., $50,000 - $100,000")
    duration = models.CharField(max_length=100, blank=True, help_text="e.g., 3 months")
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-project_date']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('portfolio:project_detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    """Additional images for a project"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.project.title} - Image {self.order}"


class Service(models.Model):
    """Services offered"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class, e.g., 'fas fa-paint-brush'")
    image = models.ImageField(upload_to='services/', blank=True)
    features = models.TextField(blank=True, help_text="List features separated by commas")
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_features_list(self):
        return [f.strip() for f in self.features.split(',') if f.strip()]
    
    def __str__(self):
        return self.name


class TeamMember(models.Model):
    """Team member profiles"""
    POSITION_CHOICES = [
        ('designer', 'Interior Designer'),
        ('architect', 'Architect'),
        ('coordinator', 'Project Coordinator'),
        ('manager', 'Project Manager'),
        ('founder', 'Founder'),
    ]
    
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='team/')
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    specialization = models.CharField(max_length=200, blank=True)
    social_links = models.JSONField(default=dict, blank=True, help_text="JSON format: {'twitter': 'url', 'linkedin': 'url'}")
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name


class Testimonial(models.Model):
    """Client testimonials"""
    client_name = models.CharField(max_length=200)
    client_position = models.CharField(max_length=200, blank=True)
    client_company = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    rating = models.PositiveIntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    client_image = models.ImageField(upload_to='testimonials/', blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_featured', 'order']
    
    def __str__(self):
        return f"Testimonial by {self.client_name}"


class BlogPost(models.Model):
    """Blog posts for design tips and insights"""
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    featured_image = models.ImageField(upload_to='blog/')
    excerpt = models.CharField(max_length=300, blank=True)
    tags = models.CharField(max_length=200, blank=True, help_text="Tags separated by commas")
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('portfolio:blog_detail', kwargs={'slug': self.slug})
    
    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    """Contact form submissions"""
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=300)
    message = models.TextField()
    project_type = models.CharField(max_length=100, blank=True)
    budget = models.CharField(max_length=100, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Message from {self.name} - {self.created_at.strftime('%Y-%m-%d')}"


class SiteSettings(models.Model):
    """Global site settings"""
    site_name = models.CharField(max_length=200, default='Ctrin Interior')
    tagline = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='site/', blank=True)
    favicon = models.ImageField(upload_to='site/', blank=True)
    
    # Contact info
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    
    # Social links
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    
    # SEO
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=200, blank=True)
    
    # Footer
    footer_text = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return self.site_name
