from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import CampusChapter, Member
import json

def chapters(request):
    chapter_list = CampusChapter.objects.filter(is_active=True).order_by('-id')
    context = {
        'chapters': chapter_list,
    }
    return render(request, 'members/campus.html', context)


def register(request):
    return render(request, 'members/registration.html')


@require_POST
def register_api(request):
    try:
        # Check if multipart or form data
        data = request.POST
        full_name = data.get('fullName', '').strip()
        name_parts = full_name.split(' ', 1)
        first_name = name_parts[0] if name_parts else 'Student'
        last_name = name_parts[1] if len(name_parts) > 1 else 'Member'

        email = data.get('email', f"student_{Member.objects.count()+1}@nabas.org.ng").strip()
        phone = data.get('phone', '').strip()
        institution = data.get('institution', '').strip()
        department = data.get('department', '').strip()
        faculty = data.get('faculty', '').strip()
        matric_number = data.get('matricNo', '').strip()
        level = data.get('level', '100').replace(' (Freshman)', '').strip()
        gender = data.get('gender', 'male').lower()
        blood_group = data.get('bloodGroup', 'O+')
        lga = data.get('lcdaArea', 'Badagry Central')
        
        existing_member = Member.objects.filter(email=email).first()
        if existing_member:
            existing_member.first_name = first_name
            existing_member.last_name = last_name
            existing_member.phone = phone
            existing_member.institution = institution
            existing_member.department = department
            existing_member.faculty = faculty
            existing_member.matric_number = matric_number
            existing_member.level = level
            existing_member.gender = gender if gender in ['male', 'female'] else 'male'
            existing_member.blood_group = blood_group
            existing_member.lga = lga
            if 'passport_photo' in request.FILES:
                existing_member.passport_photo = request.FILES['passport_photo']
            existing_member.save()
            return JsonResponse({
                'success': True,
                'id_number': existing_member.id_number,
                'full_name': existing_member.full_name,
                'message': 'Membership profile updated successfully.',
            })

        member = Member.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            institution=institution,
            department=department,
            faculty=faculty,
            matric_number=matric_number,
            level=level,
            gender=gender if gender in ['male', 'female'] else 'male',
            blood_group=blood_group,
            lga=lga,
        )

        if 'passport_photo' in request.FILES:
            member.passport_photo = request.FILES['passport_photo']
            member.save()

        return JsonResponse({
            'success': True,
            'id_number': member.id_number,
            'full_name': member.full_name,
            'message': 'Membership registered successfully in national registry.',
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def verify_member(request, id_number):
    try:
        member = Member.objects.get(id_number__iexact=id_number)
        return JsonResponse({
            'found': True,
            'id_number': member.id_number,
            'name': member.full_name,
            'institution': member.institution,
            'department': member.department,
            'is_verified': member.is_verified,
        })
    except Member.DoesNotExist:
        return JsonResponse({'found': False, 'message': 'Member ID not found'}, status=404)
