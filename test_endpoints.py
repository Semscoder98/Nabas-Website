import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nabas_project.settings')
django.setup()

from django.test import Client
from django.urls import reverse

client = Client()

routes = [
    ('home', reverse('home')),
    ('about', reverse('about')),
    ('leadership', reverse('leadership')),
    ('contact', reverse('contact')),
    ('gallery', reverse('gallery')),
    ('donate', reverse('donate')),
    ('chapters', reverse('chapters')),
    ('register', reverse('register')),
    ('news_list', reverse('news_list')),
    ('news_detail_default', reverse('news_detail_default')),
    ('programs', reverse('programs')),
    ('scholarships', reverse('scholarships')),
    ('resources', reverse('resources')),
    ('admin:index', reverse('admin:index')),
]

all_passed = True
print("Testing Django Endpoints:")
print("-" * 50)
for name, url in routes:
    response = client.get(url)
    status = response.status_code
    if status == 200 or (name == 'admin:index' and status in (200, 302)):
        print(f"[OK] [{status}] {name:20} -> {url}")
    else:
        print(f"[FAIL] [{status}] {name:20} -> {url} ERROR")
        all_passed = False

if all_passed:
    print("-" * 50)
    print("ALL ROUTES PASSED SUCCESSFULLY!")
else:
    print("SOME ROUTES FAILED.")
