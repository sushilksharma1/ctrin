from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .models import (
    Project, Category, Service, TeamMember, Testimonial,
    BlogPost, SiteSettings, ContactMessage
)
from .forms import ContactForm


def get_site_settings():
    """Get or create site settings"""
    settings_obj, _ = SiteSettings.objects.get_or_create(pk=1)
    return settings_obj


class HomeView(View):
    """Home page with featured projects, services, testimonials, and recent blog posts"""
    def get(self, request):
        featured_projects = Project.objects.filter(is_featured=True)[:6]
        featured_testimonials = Testimonial.objects.filter(is_featured=True)[:3]
        services = Service.objects.all()[:6]
        recent_posts = BlogPost.objects.filter(is_published=True)[:3]
        site_settings = get_site_settings()
        
        context = {
            'featured_projects': featured_projects,
            'featured_testimonials': featured_testimonials,
            'services': services,
            'recent_posts': recent_posts,
            'site_settings': site_settings,
        }
        return render(request, 'home.html', context)


class ProjectListView(ListView):
    """Display all projects with filtering by category"""
    model = Project
    template_name = 'projects.html'
    context_object_name = 'projects'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Project.objects.all()
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category', '')
        context['site_settings'] = get_site_settings()
        return context


class ProjectDetailView(DetailView):
    """Display single project with full details and gallery"""
    model = Project
    template_name = 'project_detail.html'
    slug_field = 'slug'
    context_object_name = 'project'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_projects'] = Project.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:3]
        context['site_settings'] = get_site_settings()
        return context


class ServiceListView(View):
    """Display all services"""
    def get(self, request):
        services = Service.objects.all()
        site_settings = get_site_settings()
        
        context = {
            'services': services,
            'site_settings': site_settings,
        }
        return render(request, 'services.html', context)


class TeamView(View):
    """Display team members"""
    def get(self, request):
        team_members = TeamMember.objects.all()
        site_settings = get_site_settings()
        
        context = {
            'team_members': team_members,
            'site_settings': site_settings,
        }
        return render(request, 'team.html', context)


class BlogListView(ListView):
    """Display all published blog posts with pagination"""
    model = BlogPost
    template_name = 'blog.html'
    context_object_name = 'posts'
    paginate_by = 9
    
    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = BlogPost.objects.filter(is_published=True)[:5]
        context['site_settings'] = get_site_settings()
        return context


class BlogDetailView(DetailView):
    """Display single blog post with related posts"""
    model = BlogPost
    template_name = 'blog_detail.html'
    slug_field = 'slug'
    context_object_name = 'post'
    
    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = BlogPost.objects.filter(is_published=True)[:5]
        context['site_settings'] = get_site_settings()
        return context


class ContactView(View):
    """Contact form page with contact information"""
    def get(self, request):
        form = ContactForm()
        site_settings = get_site_settings()
        
        context = {
            'form': form,
            'site_settings': site_settings,
        }
        return render(request, 'contact.html', context)
    
    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            
            # Send email to admin
            try:
                email_body = f"""
                New Contact Form Submission from Ctrin Interiors Website

                Name: {contact_message.name}
                Email: {contact_message.email}
                Phone: {contact_message.phone or 'Not provided'}
                Subject: {contact_message.subject}
                
                Project Type: {contact_message.project_type or 'Not specified'}
                Budget: {contact_message.budget or 'Not specified'}
                
                Message:
                {contact_message.message}
                
                ---
                This is an automated message from your website contact form.
                """
                
                send_mail(
                    subject=f"New Contact Form: {contact_message.subject}",
                    message=email_body,
                    from_email=settings.EMAIL_HOST_USER or "noreply@sierrainteriors.in",
                    recipient_list=[settings.ADMIN_EMAIL],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Email error: {e}")
            
            messages.success(request, "Thank you! Your message has been sent successfully. We'll get back to you soon.")
            return redirect('portfolio:contact')
        
        site_settings = get_site_settings()
        context = {
            'form': form,
            'site_settings': site_settings,
        }
        return render(request, 'contact.html', context)


def page_not_found(request, exception=None):
    """404 error handler"""
    site_settings = get_site_settings()
    return render(request, '404.html', {'site_settings': site_settings}, status=404)


def server_error(request):
    """500 error handler"""
    site_settings = get_site_settings()
    return render(request, '500.html', {'site_settings': site_settings}, status=500)
