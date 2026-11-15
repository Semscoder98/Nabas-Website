from django.db import models
from django.utils.text import slugify
import uuid

class CampusChapter(models.Model):
    institution_name = models.CharField(max_length=255)
    institution_code = models.CharField(max_length=50, help_text="e.g. LASU, UNILAG, LASUSTECH")
    slug = models.SlugField(unique=True, blank=True)
    state = models.CharField(max_length=100, default='Lagos')
    president_name = models.CharField(max_length=150)
    president_phone = models.CharField(max_length=30, blank=True)
    president_email = models.EmailField(blank=True)
    president_image = models.ImageField(upload_to='chapters/presidents/', blank=True, null=True)
    president_image_url = models.URLField(blank=True)
    banner = models.ImageField(upload_to='chapters/banners/', blank=True, null=True)
    banner_url = models.URLField(blank=True)
    members_count = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    meeting_venue = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['institution_name']
        verbose_name = 'Campus Chapter'
        verbose_name_plural = 'Campus Chapters'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.institution_code or self.institution_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.institution_code} - {self.institution_name}"

    @property
    def banner_display(self):
        if self.banner:
            return self.banner.url
        return self.banner_url or 'https://placehold.co/700x240/0b1a30/f5a623?text=' + (self.institution_code or 'NABAS')

    @property
    def president_photo_display(self):
        if self.president_image:
            return self.president_image.url
        return self.president_image_url or 'https://placehold.co/100x100/0b1a30/f5a623?text=Exco'


class Member(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    LEVEL_CHOICES = [
        ('100', '100 Level / ND 1'),
        ('200', '200 Level / ND 2'),
        ('300', '300 Level / HND 1'),
        ('400', '400 Level / HND 2'),
        ('500', '500 Level'),
        ('pg', 'Postgraduate'),
    ]

    id_number = models.CharField(max_length=50, unique=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30)
    institution = models.CharField(max_length=255)
    chapter = models.ForeignKey(CampusChapter, on_delete=models.SET_NULL, null=True, blank=True, related_name='members')
    faculty = models.CharField(max_length=150, blank=True)
    department = models.CharField(max_length=150)
    matric_number = models.CharField(max_length=100)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='100')
    blood_group = models.CharField(max_length=10, blank=True, default='O+')
    date_of_birth = models.DateField(null=True, blank=True)
    state_of_origin = models.CharField(max_length=100, default='Lagos')
    lga = models.CharField(max_length=100, default='Badagry')
    hometown_division = models.CharField(max_length=100, blank=True, help_text="e.g. Ajara, Badagry Central, Ogu, etc.")
    passport_photo = models.ImageField(upload_to='members/passports/', blank=True, null=True)
    is_verified = models.BooleanField(default=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-registered_at']
        verbose_name = 'Registered Member'
        verbose_name_plural = 'Registered Members'

    def save(self, *args, **kwargs):
        if not self.id_number:
            # Generate ID like NABAS/2026/00142
            count = Member.objects.count() + 1
            self.id_number = f"NABAS/2026/{count:05d}"
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        parts = [self.first_name, self.middle_name, self.last_name]
        return " ".join([p for p in parts if p]).strip()

    @property
    def photo_url(self):
        if self.passport_photo:
            return self.passport_photo.url
        return 'https://placehold.co/300x300/0b1a30/f5a623?text=Passport'

    def __str__(self):
        return f"{self.full_name} ({self.id_number})"
