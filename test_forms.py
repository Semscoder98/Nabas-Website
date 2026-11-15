import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nabas_project.settings')
django.setup()

from django.test import Client
from django.urls import reverse
from core.models import ContactMessage, Donation
from members.models import Member

client = Client()

print("Testing Form Submissions & Database Integration:")
print("-" * 50)

# 1. Contact Form POST
resp_contact = client.post(reverse('contact'), {
    'name': 'Test Student',
    'email': 'teststudent@example.com',
    'phone': '+234 801 234 5678',
    'subject': 'Membership ID Inquiry',
    'message': 'Testing contact submission from Badagry.',
}, follow=True)

contact_exists = ContactMessage.objects.filter(email='teststudent@example.com').exists()
print(f"Contact Form Submission: {'[SUCCESS]' if contact_exists else '[FAILED]'}")

# 2. Donation Form POST
resp_donate = client.post(reverse('donate'), {
    'donor_name': 'Chief Akran Supporter',
    'email': 'patron@example.com',
    'phone': '+234 809 111 2233',
    'amount': 50000,
    'purpose': 'Annual Bursary Endowment',
}, follow=True)

donation_exists = Donation.objects.filter(email='patron@example.com').exists()
print(f"Donation Form Submission: {'[SUCCESS]' if donation_exists else '[FAILED]'}")

# 3. Member Registration API POST
resp_member = client.post(reverse('register_api'), {
    'fullName': 'Mauyon Sewedo Wheto',
    'email': 'mauyon.wheto@example.com',
    'phone': '+234 812 333 4455',
    'institution': 'Lagos State University',
    'faculty': 'Faculty of Science',
    'department': 'Computer Science',
    'matricNo': '220591042',
    'level': '300',
    'gender': 'Male',
    'bloodGroup': 'O+',
    'lcdaArea': 'Badagry Central',
})

member_exists = Member.objects.filter(email='mauyon.wheto@example.com').exists()
print(f"Member Registration API: {'[SUCCESS]' if member_exists else '[FAILED]'}")

if contact_exists and donation_exists and member_exists:
    member = Member.objects.get(email='mauyon.wheto@example.com')
    print(f"Generated Member ID: {member.id_number} for {member.full_name}")
    print("-" * 50)
    print("ALL FORMS TESTED AND VERIFIED SUCCESSFULLY!")
