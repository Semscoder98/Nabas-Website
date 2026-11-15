from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Program, Scholarship, Resource, EventRegistration

def program_list(request):
    upcoming_programs = Program.objects.filter(is_upcoming=True).order_by('-id')
    past_programs = Program.objects.filter(is_upcoming=False).order_by('-id')
    
    # In case no programs have been marked is_upcoming=False yet, all can be accessed
    context = {
        'upcoming_programs': upcoming_programs,
        'past_programs': past_programs,
        'all_programs': Program.objects.all().order_by('-id'),
    }
    return render(request, 'programs/program_list.html', context)


def program_detail(request, slug):
    program = get_object_or_404(Program, slug=slug)
    related_programs = Program.objects.exclude(pk=program.pk).filter(is_upcoming=True)[:3]

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        institution = request.POST.get('institution', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()

        if full_name and phone and email:
            EventRegistration.objects.create(
                program=program,
                full_name=full_name,
                institution=institution,
                phone=phone,
                email=email,
            )
            messages.success(request, f"Registration confirmed! You have successfully reserved a seat for '{program.title}'.")
            return redirect('program_detail', slug=program.slug)
        else:
            messages.error(request, "Please fill in all required registration fields.")

    context = {
        'program': program,
        'related_programs': related_programs,
    }
    return render(request, 'programs/program_detail.html', context)


def scholarship_list(request):
    scholarships = Scholarship.objects.all().order_by('-is_open', '-created_at', '-id')
    context = {
        'scholarships': scholarships,
    }
    return render(request, 'programs/scholarship_list.html', context)


from django.db.models import F

def resource_list(request):
    category = request.GET.get('category')
    search_query = request.GET.get('search')
    resources = Resource.objects.all().order_by('-uploaded_at', '-id')

    if category:
        resources = resources.filter(category=category)

    if search_query:
        resources = resources.filter(title__icontains=search_query)

    context = {
        'resources': resources,
        'category_choices': Resource.CATEGORY_CHOICES,
        'selected_category': category,
        'search_query': search_query,
    }
    return render(request, 'programs/resource_list.html', context)


def download_resource(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    # Increment download count atomically
    Resource.objects.filter(pk=pk).update(downloads_count=F('downloads_count') + 1)
    
    if resource.file:
        return redirect(resource.file.url)
    elif resource.file_url:
        return redirect(resource.file_url)
    return redirect('resources')

