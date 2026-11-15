from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage, ExecutiveMember, GalleryImage, Donation, Partner
from news.models import Article
from programs.models import Program
from members.models import CampusChapter, Member

from django.db.models import Q

def home(request):
    featured_news = Article.objects.filter(is_published=True).order_by('-created_at', '-id')[:3]
    upcoming_events = Program.objects.filter(is_upcoming=True).order_by('-id')[:3]
    president = ExecutiveMember.objects.filter(portfolio='exec', is_spotlight=True, is_past_leader=False).first() or ExecutiveMember.objects.filter(portfolio='exec', is_past_leader=False).first()
    gallery_images = GalleryImage.objects.all().order_by('-created_at', '-id')[:5]
    chapters_count = CampusChapter.objects.filter(is_active=True).count() or 20
    members_count = Member.objects.count() or 5000
    partners = Partner.objects.filter(is_active=True).order_by('order', '-id')

    context = {
        'featured_news': featured_news,
        'upcoming_events': upcoming_events,
        'president': president,
        'gallery_images': gallery_images,
        'chapters_count': chapters_count,
        'members_count': members_count,
        'partners': partners,
    }
    return render(request, 'core/index.html', context)



def about(request):
    return render(request, 'core/about.html')


def leadership(request):
    # Student Executive Council (SEC)
    sec_spotlight = ExecutiveMember.objects.filter(portfolio='exec', is_spotlight=True, is_past_leader=False).first()
    sec_members = ExecutiveMember.objects.filter(portfolio='exec', is_spotlight=False, is_past_leader=False)
    
    # Student Parliamentary Council (SPC)
    spc_spotlight = ExecutiveMember.objects.filter(portfolio='leg', is_spotlight=True, is_past_leader=False).first()
    spc_members = ExecutiveMember.objects.filter(portfolio='leg', is_spotlight=False, is_past_leader=False)
    
    # Directorates & Special Appointees
    directorate_spotlight = ExecutiveMember.objects.filter(portfolio='directorate', is_spotlight=True, is_past_leader=False).first()
    directorate_members = ExecutiveMember.objects.filter(portfolio='directorate', is_spotlight=False, is_past_leader=False)
    
    # Patrons & Advisory Council
    advisory_spotlight = ExecutiveMember.objects.filter(portfolio='advisory', is_spotlight=True, is_past_leader=False).first()
    advisory_members = ExecutiveMember.objects.filter(portfolio='advisory', is_spotlight=False, is_past_leader=False)
    
    # Past Leaders (Hall of Fame)
    past_leaders = ExecutiveMember.objects.filter(Q(portfolio='past') | Q(is_past_leader=True))
    
    # All active leaders for dynamic modals
    all_leaders = ExecutiveMember.objects.all()

    context = {
        'sec_spotlight': sec_spotlight,
        'sec_members': sec_members,
        'sec_count': (1 if sec_spotlight else 0) + sec_members.count(),
        
        'spc_spotlight': spc_spotlight,
        'spc_members': spc_members,
        'spc_count': (1 if spc_spotlight else 0) + spc_members.count(),
        
        'directorate_spotlight': directorate_spotlight,
        'directorate_members': directorate_members,
        'directorate_count': (1 if directorate_spotlight else 0) + directorate_members.count(),
        
        'advisory_spotlight': advisory_spotlight,
        'advisory_members': advisory_members,
        'advisory_count': (1 if advisory_spotlight else 0) + advisory_members.count(),
        
        'past_leaders': past_leaders,
        'past_count': past_leaders.count(),
        
        'all_leaders': all_leaders,
    }
    return render(request, 'core/leadership.html', context)


from django.http import JsonResponse

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        subject = request.POST.get('subject', 'General Inquiry').strip()
        message = request.POST.get('message', '').strip()

        if name and email and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=message,
            )
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.POST.get('ajax') == '1':
                return JsonResponse({
                    'success': True,
                    'message': 'Thank you! Your message has been sent to the NABAS Secretariat. We will respond promptly.'
                })
            return redirect('contact')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.POST.get('ajax') == '1':
                return JsonResponse({
                    'success': False,
                    'message': 'Please fill in all required fields before submitting.'
                }, status=400)
            messages.error(request, "Please fill in all required fields before submitting.")

    return render(request, 'core/contact.html')


def gallery(request):
    images = GalleryImage.objects.all().order_by('-created_at', '-id')
    context = {
        'images': images,
    }
    return render(request, 'core/gallery.html', context)


def donate(request):
    if request.method == 'POST':
        donor_name = request.POST.get('donor_name') or request.POST.get('fullname') or 'Anonymous Donor'
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        amount = request.POST.get('amount', 5000)
        purpose = request.POST.get('purpose', 'General Student Welfare')

        try:
            Donation.objects.create(
                donor_name=donor_name,
                email=email or 'donor@nabas.org.ng',
                phone=phone,
                amount=amount,
                purpose=purpose,
                status='successful',
            )
            messages.success(request, f"Thank you, {donor_name}! Your donation of ₦{amount:,} has been recorded. Your support impacts Badagry students across all institutions.")
        except Exception:
            messages.error(request, "Could not process donation record. Please try again.")

        return redirect('donate')

    return render(request, 'core/donate.html')
