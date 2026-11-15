from django.db import models
from django.utils.text import slugify

class Program(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, max_length=255)
    theme = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    date = models.CharField(max_length=150, help_text="e.g. November 14 - 18, 2026")
    time = models.CharField(max_length=100, blank=True, default="9:00 AM – 3:00 PM WAT")
    venue = models.CharField(max_length=255)
    target_audience = models.CharField(max_length=200, blank=True, default="Open to All Badagry Tertiary Students")
    image = models.ImageField(upload_to='programs/', blank=True, null=True)
    image_url = models.URLField(blank=True, help_text="External image link fallback")
    category = models.CharField(max_length=100, default='Annual Event')
    status = models.CharField(max_length=50, default='Registration Open', blank=True)
    is_upcoming = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    # Impact Archive Fields (for past programmes)
    impact_summary = models.TextField(blank=True, help_text="Summary of impact, attendees, and highlights for concluded programs")
    impact_stat_1_num = models.CharField(max_length=50, blank=True, default="500+")
    impact_stat_1_label = models.CharField(max_length=50, blank=True, default="Delegates")
    impact_stat_2_num = models.CharField(max_length=50, blank=True, default="22")
    impact_stat_2_label = models.CharField(max_length=50, blank=True, default="Chapters")
    impact_stat_3_num = models.CharField(max_length=50, blank=True, default="₦1.2M")
    impact_stat_3_label = models.CharField(max_length=50, blank=True, default="Prizes Awarded")

    class Meta:
        ordering = ['-id']
        verbose_name = 'Program & Event'
        verbose_name_plural = 'Programs & Events'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        return self.image_url or 'https://images.unsplash.com/photo-1517486808906-6ca8b3f04846?auto=format&fit=crop&w=800&q=80'


class EventRegistration(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='registrations')
    full_name = models.CharField(max_length=200)
    institution = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-registered_at']
        verbose_name = 'Event Registration'
        verbose_name_plural = 'Event Registrations'

    def __str__(self):
        return f"{self.full_name} - {self.program.title}"


class Scholarship(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, max_length=255)
    donor_organization = models.CharField(max_length=200, help_text="e.g. Badagry Division Education Fund")
    description = models.TextField()
    eligibility = models.TextField(help_text="Key requirements")
    award_amount = models.CharField(max_length=100, help_text="e.g. ₦150,000 / Session")
    deadline = models.CharField(max_length=100, help_text="e.g. October 30, 2026")
    application_link = models.URLField(blank=True, help_text="External application portal URL if any")
    image = models.ImageField(upload_to='scholarships/', blank=True, null=True, help_text="Optional cover image")
    is_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_open', '-created_at']
        verbose_name = 'Scholarship'
        verbose_name_plural = 'Scholarships'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Resource(models.Model):
    CATEGORY_CHOICES = [
        ('constitution', 'Constitution & Governance'),
        ('bursary', 'Bursary & Scholarships'),
        ('academic', 'Academic Guides'),
        ('past_questions', 'Past Exam & Aptitude Questions'),
        ('forms', 'Forms & Templates'),
        ('media', 'Media & Press Kit'),
        ('communique', 'Communique & Resolutions'),
    ]

    title = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='academic')
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='resources/', blank=True, null=True)
    file_url = models.URLField(blank=True, help_text="External download link if hosted elsewhere")
    file_size = models.CharField(max_length=50, blank=True, help_text="Automatically calculated from uploaded file, or specify custom/external size")
    downloads_count = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Resource / Download'
        verbose_name_plural = 'Resources & Downloads'

    def save(self, *args, **kwargs):
        # Automatically detect and format file size when a file is uploaded
        if self.file and hasattr(self.file, 'size'):
            try:
                size_bytes = self.file.size
                if size_bytes < 1024:
                    self.file_size = f"{size_bytes} B"
                elif size_bytes < 1024 * 1024:
                    self.file_size = f"{size_bytes / 1024:.1f} KB"
                elif size_bytes < 1024 * 1024 * 1024:
                    self.file_size = f"{size_bytes / (1024 * 1024):.1f} MB"
                else:
                    self.file_size = f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"
            except Exception:
                pass
        elif not self.file_size and self.file_url:
            self.file_size = "External Link"
        elif not self.file_size:
            self.file_size = "Document"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"

    @property
    def download_url(self):
        if self.file:
            return self.file.url
        return self.file_url or '#'
