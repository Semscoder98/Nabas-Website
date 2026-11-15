import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nabas_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import ExecutiveMember, GalleryImage
from members.models import CampusChapter, Member
from news.models import Category, Article
from programs.models import Program, Scholarship, Resource

User = get_user_model()

def seed():
    print("Seeding database...")

    # 1. Create Superuser
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@nabas.org.ng', 'admin123')
        print("Created superuser: admin / admin123")
    else:
        print("Superuser admin already exists.")

    # 2. Campus Chapters
    chapters_data = [
        {
            'name': 'Lagos State University',
            'code': 'LASU',
            'state': 'Lagos',
            'president': 'Comr. Akande Gabriel Posu',
            'phone': '+234 802 345 6789',
            'members': 1420,
            'venue': 'Faculty of Arts Auditorium, LASU Ojo Campus',
            'description': 'One of the premier and largest chapters of NABAS representing Badagry indigenes across all LASU faculties.',
        },
        {
            'name': 'University of Lagos',
            'code': 'UNILAG',
            'state': 'Lagos',
            'president': 'Comr. Senapon Rachel Hundeyin',
            'phone': '+234 803 987 6543',
            'members': 850,
            'venue': 'Sub-hall 4, Student Union Building, Akoka',
            'description': 'Dynamic and active chapter fostering academic excellence and student networking at Akoka.',
        },
        {
            'name': 'Lagos State University of Science and Technology',
            'code': 'LASUSTECH',
            'state': 'Lagos',
            'president': 'Comr. Emmanuel Wheto',
            'phone': '+234 810 555 4321',
            'members': 730,
            'venue': 'Engineering Complex B, Ikorodu Campus',
            'description': 'Leading technology and innovation chapter driving student technical empowerment.',
        },
        {
            'name': 'Lagos State University of Education',
            'code': 'LASUED',
            'state': 'Lagos',
            'president': 'Comr. Kemi Sewedo Hunpatin',
            'phone': '+234 818 222 3344',
            'members': 910,
            'venue': 'Main Campus Hall, Oto/Ijanikin',
            'description': 'Proximity chapter deeply connected with community educational outreach programs.',
        },
        {
            'name': 'Yaba College of Technology',
            'code': 'YABATECH',
            'state': 'Lagos',
            'president': 'Comr. Michael Boyon Meto',
            'phone': '+234 805 111 8899',
            'members': 620,
            'venue': 'Bakassi Hall, Yaba Campus',
            'description': 'Fostering vocational mastery, technical skills, and leadership for polytechnic scholars.',
        },
    ]

    for item in chapters_data:
        chapter, created = CampusChapter.objects.get_or_create(
            institution_code=item['code'],
            defaults={
                'institution_name': item['name'],
                'state': item['state'],
                'president_name': item['president'],
                'president_phone': item['phone'],
                'members_count': item['members'],
                'meeting_venue': item['venue'],
                'description': item['description'],
            }
        )
        if created:
            print(f"Created chapter: {chapter}")

    # 3. Executives
    exco_data = [
        {
            'name': 'Comr. Boyon John Metonno',
            'role': 'President',
            'portfolio': 'exec',
            'institution': 'Lagos State University (LASU)',
            'bio': 'Passionate student advocate committed to educational equity, welfare, and sustainable human capacity building for Badagry students across all Nigerian universities.',
            'order': 1,
            'image_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=600&q=80',
        },
        {
            'name': 'Comr. Senapon Joy Avoseh',
            'role': 'Vice President',
            'portfolio': 'exec',
            'institution': 'University of Lagos (UNILAG)',
            'bio': 'Dedicated to female student participation, academic mentoring initiatives, and institutional relations.',
            'order': 2,
            'image_url': 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=600&q=80',
        },
        {
            'name': 'Comr. Mauyon Michael Hunpe',
            'role': 'General Secretary',
            'portfolio': 'exec',
            'institution': 'LASUSTECH',
            'bio': 'Administrator driving secretariat operations, official communiqués, and national records management.',
            'order': 3,
            'image_url': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=600&q=80',
        },
        {
            'name': 'Comr. Setonji David Wheto',
            'role': 'Treasurer & Financial Secretary',
            'portfolio': 'exec',
            'institution': 'LASUED',
            'bio': 'Ensuring accountability, transparent financial stewardship, and bursary disbursements.',
            'order': 4,
            'image_url': 'https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?auto=format&fit=crop&w=600&q=80',
        },
        {
            'name': 'Comr. Posu Peter Akande',
            'role': 'Public Relations Officer (PRO)',
            'portfolio': 'exec',
            'institution': 'YABATECH',
            'bio': 'Chief information officer managing media broadcasts, digital channels, and community relations.',
            'order': 5,
            'image_url': 'https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?auto=format&fit=crop&w=600&q=80',
        },
        # Directorates (Appointed Offices across Institutions & Organizations)
        {
            'name': 'Comr. Sewedo Emmanuel Hunpatin',
            'role': 'Director of ICT & Digital Innovation',
            'tag': 'ICT Directorate',
            'portfolio': 'directorate',
            'institution': 'Badagry Tech & Innovation Hub / LASUSTECH',
            'bio': 'Appointed to lead digital infrastructure, student portal engineering, and tech capacity partnerships across partner institutions.',
            'responsibilities': 'Oversees the NABAS digital membership portal and tech bootcamps\nCoordinates with partner tech hubs and tertiary ICT directorates\nLeads digital literacy and software training initiatives',
            'order': 1,
            'image_url': 'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&w=600&q=80',
        },
        {
            'name': 'Comr. Senami Grace Zannu',
            'role': 'Director of Gender, Youth & Diaspora Affairs',
            'tag': 'Diaspora & Gender',
            'portfolio': 'directorate',
            'institution': 'Lagos State Youth Council / UNILAG',
            'bio': 'Appointed liaison representing Badagry students in youth development agencies, female empowerment coalitions, and diaspora networks.',
            'responsibilities': 'Liaises with state youth ministries and civil society organizations\nCoordinates female undergraduate mentorship and welfare drives\nConnects diaspora Badagry scholars with home opportunities',
            'order': 2,
            'image_url': 'https://images.unsplash.com/photo-1531123897727-8f129e1688ce?auto=format&fit=crop&w=600&q=80',
        },
        {
            'name': 'Comr. Jesuton Paul Gbenu',
            'role': 'Director of Inter-Governmental & Bursary Liaison',
            'tag': 'Bursary Liaison',
            'portfolio': 'directorate',
            'institution': 'Lagos State Scholarship Board / LASU Liaison',
            'bio': 'Special appointee interfacing with local councils, scholarship boards, and educational trusts to facilitate seamless bursary verification.',
            'responsibilities': 'Interfaces with Badagry LG, Olorunda LCDA, and Badagry West LCDA education desks\nAssists indigenous students with Lagos State Scholarship Board documentation\nTracks institutional grant and bursary disbursements',
            'order': 3,
            'image_url': 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=600&q=80',
        },
        {
            'name': 'Comr. Mauyon Esther Vothon',
            'role': 'Director of Research, Policy & Academic Documentation',
            'tag': 'Research & Policy',
            'portfolio': 'directorate',
            'institution': 'Badagry Heritage Research Centre / UI',
            'bio': 'Appointed to coordinate undergraduate research publications, policy briefs, and educational resource repositories across tertiary chapters.',
            'responsibilities': 'Curates the NABAS academic past questions and thesis repository\nConvenes inter-institutional research and policy dialogues\nPartners with academic bodies and cultural research institutes',
            'order': 4,
            'image_url': 'https://images.unsplash.com/photo-1548142813-c348350df52b?auto=format&fit=crop&w=600&q=80',
        },
    ]

    for item in exco_data:
        exco, created = ExecutiveMember.objects.get_or_create(
            name=item['name'],
            defaults={
                'role': item['role'],
                'tag': item.get('tag', ''),
                'portfolio': item['portfolio'],
                'institution': item['institution'],
                'bio': item['bio'],
                'responsibilities': item.get('responsibilities', ''),
                'order': item['order'],
                'image_url': item['image_url'],
            }
        )
        if created:
            print(f"Created executive: {exco}")

    # 4. News Categories and Articles
    cat_general, _ = Category.objects.get_or_create(name='General News')
    cat_bursary, _ = Category.objects.get_or_create(name='Bursary & Grants')
    cat_communique, _ = Category.objects.get_or_create(name='Official Communiqués')
    cat_campus, _ = Category.objects.get_or_create(name='Campus Spotlight')

    articles_data = [
        {
            'title': 'NABAS National Convention 2026: Badagry Students Set New Academic Agenda',
            'category': cat_general,
            'excerpt': 'Delegates from 20 tertiary institutions gathered in Badagry to deliberate on student welfare, scholarship accessibility, and innovation hubs.',
            'content': """The National Association of Badagry Students (NABAS) has successfully concluded its 2026 National Annual Convention held at the Badagry Local Government Multi-purpose Hall.

Over 500 accredited student leaders and delegates representing chapters across federal, state, and private tertiary institutions attended the 3-day symposium themed "Education as the Bedrock for Cultural and Economic Renaissance in Badagry".

Resolutions reached included the formal launch of the NABAS Digital ID Card, expansion of the Academic Endowment Fund, and partnerships with local community stakeholders to secure more tertiary bursary slots for indigenous youths.""",
            'image_url': 'https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=800&q=80',
            'is_featured': True,
        },
        {
            'title': 'Lagos State Bursary Verification Exercise: Important Notice for Badagry Indigenes',
            'category': cat_bursary,
            'excerpt': 'The Lagos State Scholarship Board has scheduled physical and digital verification for all Badagry Division applicants for the 2026 session.',
            'content': """The Central Executive Council of NABAS wishes to inform all indigenous students of Badagry division who applied for the Lagos State Scholarship and Bursary award that the verification exercise has officially commenced.

Applicants are advised to gather their letter of admission, valid institutional ID card, local government identification certificate, and LASRRA registration cards. NABAS chapter coordinators will be stationed at key campuses to guide students through the documentation process.""",
            'image_url': 'https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?auto=format&fit=crop&w=700&q=80',
            'is_featured': True,
        },
        {
            'title': 'NABAS Launches Free Tech Skills & Coding Bootcamp for Tertiary Scholars',
            'category': cat_campus,
            'excerpt': 'In collaboration with Badagry Innovation Hub, NABAS announces a 6-week intensive software engineering and data analytics training program.',
            'content': """As part of our commitment to preparing Badagry youths for the future of work, NABAS has partnered with tech organizations to offer 100 fully sponsored seats in Frontend Web Development, Python Programming, and Product Design.

Classes will be delivered both virtually and at the Badagry Resource Centre with mentors assigned to each student team. Registration is open to all registered NABAS members with valid digital student IDs.""",
            'image_url': 'https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=800&q=80',
            'is_featured': False,
        },
    ]

    for item in articles_data:
        art, created = Article.objects.get_or_create(
            title=item['title'],
            defaults={
                'category': item['category'],
                'excerpt': item['excerpt'],
                'content': item['content'],
                'image_url': item['image_url'],
                'is_featured': item['is_featured'],
            }
        )
        if created:
            print(f"Created article: {art}")

    # 5. Programs
    programs_data = [
        {
            'title': 'Annual Badagry Students Leadership Summit',
            'theme': 'Empowering Tomorrow Leaders Today',
            'date': 'November 14 - 16, 2026',
            'venue': 'Badagry Local Government Secretariat Hall',
            'description': 'A three-day flagship conference bringing together student leaders, seasoned policymakers, and industry executives.',
            'image_url': 'https://images.unsplash.com/photo-1511632765486-a01980e01a18?auto=format&fit=crop&w=800&q=80',
            'category': 'Flagship Conference',
        },
        {
            'title': 'Badagry Heritage & Cultural Festival',
            'theme': 'Celebrating Our Ancestral Roots & Unity',
            'date': 'December 22 - 24, 2026',
            'venue': 'Whispering Palms Resort & Historic Heritage Grounds, Badagry',
            'description': 'Annual celebration showcasing Badagry arts, language, drama, boat regattas, and academic exhibitions.',
            'image_url': 'https://images.unsplash.com/photo-1529156069898-49953e39b3ac?auto=format&fit=crop&w=800&q=80',
            'category': 'Cultural Day',
        },
        {
            'title': 'NABAS Inter-Campus Quiz & Debate Championship',
            'theme': 'Intellectual Vigour for Badagry Advancement',
            'date': 'January 18, 2027',
            'venue': 'LASU Main Auditorium, Ojo',
            'description': 'High-stakes debate between campus chapters with prizes, medals, and academic textbooks for winning chapters.',
            'image_url': 'https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&fit=crop&w=800&q=80',
            'category': 'Academic Competition',
        },
    ]

    for item in programs_data:
        prog, created = Program.objects.get_or_create(
            title=item['title'],
            defaults={
                'theme': item['theme'],
                'date': item['date'],
                'venue': item['venue'],
                'description': item['description'],
                'image_url': item['image_url'],
                'category': item['category'],
            }
        )
        if created:
            print(f"Created program: {prog}")

    # 6. Scholarships
    scholarships_data = [
        {
            'title': 'Badagry Division Higher Education Bursary Scheme 2026',
            'donor': 'Badagry Divisional Council & Education Trust',
            'description': 'Annual financial assistance grant for indigenes in 200 level and above across accredited Nigerian public universities and polytechnics.',
            'eligibility': 'Must be an indigene of Badagry Local Government / Olorunda / Badagry West LCDAs with minimum CGPA of 2.50.',
            'award': '₦100,000 / Academic Session',
            'deadline': 'November 30, 2026',
        },
        {
            'title': 'Akran of Badagry Academic Excellence Merit Award',
            'donor': 'Royal Palace of the Akran of Badagry Kingdom',
            'description': 'Merit scholarship honoring high-achieving Badagry scholars maintaining first-class or distinction standing.',
            'eligibility': 'Enrolled undergraduate or HND students with CGPA >= 4.50 (or Distinction in Polytechnics).',
            'award': '₦250,000 + Commendation Certificate',
            'deadline': 'December 15, 2026',
        },
    ]

    for item in scholarships_data:
        sch, created = Scholarship.objects.get_or_create(
            title=item['title'],
            defaults={
                'donor_organization': item['donor'],
                'description': item['description'],
                'eligibility': item['eligibility'],
                'award_amount': item['award'],
                'deadline': item['deadline'],
            }
        )
        if created:
            print(f"Created scholarship: {sch}")

    # 7. Resources
    resources_data = [
        {
            'title': 'NABAS Official Constitution & By-Laws (Amended 2026)',
            'category': 'constitution',
            'description': 'The supreme document governing the legislative, executive, and judicial affairs of the National Association of Badagry Students.',
            'file_size': '2.4 MB',
        },
        {
            'title': 'General Studies (GNS 101/102) Comprehensive Revision Past Questions',
            'category': 'past_questions',
            'description': 'Unified collection of past examination questions, answers, and study notes compiled by top graduating Badagry scholars.',
            'file_size': '5.8 MB',
        },
        {
            'title': 'Undergraduate Research Methodology & Thesis Guide',
            'category': 'academic',
            'description': 'Step-by-step handbook covering proposal drafting, literature review, data analysis, and citation standards for final year students.',
            'file_size': '3.1 MB',
        },
    ]

    for item in resources_data:
        res, created = Resource.objects.get_or_create(
            title=item['title'],
            defaults={
                'category': item['category'],
                'description': item['description'],
                'file_size': item['file_size'],
            }
        )
        if created:
            print(f"Created resource: {res}")

    # 8. Gallery
    gallery_data = [
        {'title': 'National Convention Opening Ceremony', 'category': 'events', 'image_url': 'https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=600&q=80'},
        {'title': 'Badagry Heritage Arch Tour', 'category': 'cultural', 'image_url': 'https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?auto=format&fit=crop&w=600&q=80'},
        {'title': 'Student Leadership Workshop', 'category': 'leadership', 'image_url': 'https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=600&q=80'},
        {'title': 'Inter-Campus Quiz Finalists', 'category': 'academic', 'image_url': 'https://images.unsplash.com/photo-1517486808906-6ca8b3f04846?auto=format&fit=crop&w=600&q=80'},
        {'title': 'Annual Cultural Regatta & Day', 'category': 'cultural', 'image_url': 'https://images.unsplash.com/photo-1511632765486-a01980e01a18?auto=format&fit=crop&w=600&q=80'},
        {'title': 'Digital Skills Bootcamp Cohort', 'category': 'events', 'image_url': 'https://images.unsplash.com/photo-1524178232363-1fb2b075b655?auto=format&fit=crop&w=600&q=80'},
    ]

    for item in gallery_data:
        gal, created = GalleryImage.objects.get_or_create(
            title=item['title'],
            defaults={
                'category': item['category'],
                'image_url': item['image_url'],
            }
        )
        if created:
            print(f"Created gallery item: {gal}")

    print("\nDatabase seeded successfully!")

if __name__ == '__main__':
    seed()
