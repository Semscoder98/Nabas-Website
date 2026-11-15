from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f"{self.name} - {self.subject}"


class ExecutiveMember(models.Model):
    PORTFOLIO_CHOICES = [
        ('exec', 'Student Executive Council (SEC)'),
        ('leg', 'Student Parliamentary Council (SPC)'),
        ('directorate', 'Directorates & Special Appointees'),
        ('advisory', 'Patrons & Advisory Council'),
        ('past', 'Past Leaders (Hall of Fame)'),
    ]

    name = models.CharField(max_length=150)
    role = models.CharField(max_length=150)
    tag = models.CharField(max_length=100, blank=True, help_text="Badge tag e.g. President, Speaker, Chief Whip, Vice President")
    portfolio = models.CharField(max_length=50, choices=PORTFOLIO_CHOICES, default='exec', help_text="Council Arm")
    institution = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='executives/', blank=True, null=True)
    image_url = models.URLField(blank=True, help_text="External image link fallback")
    bio = models.TextField(blank=True)
    quote = models.TextField(blank=True, help_text="Personal quote or motto (featured on spotlight cards)")
    responsibilities = models.TextField(blank=True, help_text="Key responsibilities / statutory duties (one per line)")
    tenure = models.CharField(max_length=100, default='2025 – 2026', help_text="e.g. 2025 – 2026")
    is_spotlight = models.BooleanField(default=False, help_text="Spotlight featured leader (e.g. President, Speaker, Chief Patron)")
    is_past_leader = models.BooleanField(default=False, help_text="Mark as past leader (moved to Past Leaders)")
    order = models.PositiveIntegerField(default=0, help_text="Sort display order")
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    linkedin_url = models.URLField(blank=True, verbose_name="LinkedIn URL")
    twitter_url = models.URLField(blank=True, verbose_name="X (Twitter) URL")
    facebook_url = models.URLField(blank=True, verbose_name="Facebook URL")

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Leader / Council Member'
        verbose_name_plural = 'Leadership & Council Members'

    def __str__(self):
        return f"{self.name} ({self.role})"

    @property
    def photo(self):
        if self.image:
            return self.image.url
        return self.image_url or 'https://placehold.co/400x400/0c1d36/f5b301?text=NABAS+Leader'

    @property
    def display_tag(self):
        return self.tag or self.role

    @property
    def clean_quote(self):
        if not self.quote:
            return ""
        from django.utils.html import strip_tags
        cleaned = strip_tags(self.quote).replace('&nbsp;', ' ').strip()
        cleaned = cleaned.strip('"\'“”')
        return cleaned

    @property
    def clean_bio(self):
        if not self.bio:
            return ""
        from django.utils.html import strip_tags
        return strip_tags(self.bio).replace('&nbsp;', ' ').strip()

    @property
    def responsibilities_list(self):
        if not self.responsibilities:
            return []
        import re
        from django.utils.html import strip_tags
        raw = self.responsibilities
        text = re.sub(r'</?(?:p|li|div|h\d|tr|br)[^>]*>', '\n', raw, flags=re.IGNORECASE)
        text = strip_tags(text)
        lines = []
        for line in text.split('\n'):
            cleaned = line.strip().lstrip('•-*123456789. ').replace('&nbsp;', ' ').strip()
            if cleaned:
                lines.append(cleaned)
        return lines


class ExecutiveCouncilMember(ExecutiveMember):
    class Meta:
        proxy = True
        verbose_name = 'Executive Council Member'
        verbose_name_plural = '1. Executive Council (SEC)'

    def save(self, *args, **kwargs):
        if not self.portfolio or self.portfolio != 'past':
            self.portfolio = 'exec'
        super().save(*args, **kwargs)


class ParliamentaryCouncilMember(ExecutiveMember):
    class Meta:
        proxy = True
        verbose_name = 'Parliamentary Council Member'
        verbose_name_plural = '2. Parliamentary Council (SPC)'

    def save(self, *args, **kwargs):
        if not self.portfolio or self.portfolio != 'past':
            self.portfolio = 'leg'
        super().save(*args, **kwargs)


class DirectorateMember(ExecutiveMember):
    class Meta:
        proxy = True
        verbose_name = 'Directorate Appointee'
        verbose_name_plural = '3. Directorates'

    def save(self, *args, **kwargs):
        if not self.portfolio or self.portfolio != 'past':
            self.portfolio = 'directorate'
        super().save(*args, **kwargs)


class AdvisoryCouncilMember(ExecutiveMember):
    class Meta:
        proxy = True
        verbose_name = 'Patron & Advisor'
        verbose_name_plural = '4. Patrons & Advisory Council'

    def save(self, *args, **kwargs):
        if not self.portfolio or self.portfolio != 'past':
            self.portfolio = 'advisory'
        super().save(*args, **kwargs)


class PastLeader(ExecutiveMember):
    class Meta:
        proxy = True
        verbose_name = 'Past Leader'
        verbose_name_plural = '5. Past Leaders (Hall of Fame)'

    def save(self, *args, **kwargs):
        self.is_past_leader = True
        self.portfolio = 'past'
        self.is_spotlight = False
        super().save(*args, **kwargs)


class GalleryImage(models.Model):
    CATEGORY_CHOICES = [
        ('all', 'General'),
        ('events', 'Events & Hangouts'),
        ('academic', 'Academic Seminars'),
        ('cultural', 'Cultural Heritage'),
        ('leadership', 'Leadership Summits'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='events')
    image = models.ImageField(upload_to='gallery/', blank=True, null=True)
    image_url = models.URLField(blank=True, help_text="External image link fallback")
    caption = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Gallery Image'
        verbose_name_plural = 'Gallery Images'

    def __str__(self):
        return self.title

    @property
    def display_url(self):
        if self.image:
            return self.image.url
        return self.image_url or 'https://placehold.co/600x400/0c1d36/f5b301?text=NABAS'


class Donation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('successful', 'Successful'),
        ('failed', 'Failed'),
    ]

    donor_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    purpose = models.CharField(max_length=100, default='General Fund')
    reference = models.CharField(max_length=100, unique=True, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.donor_name} - ₦{self.amount} ({self.status})"


class Partner(models.Model):
    CATEGORY_CHOICES = [
        ('government', 'Government Agency'),
        ('education', 'Education Partner'),
        ('corporate', 'Corporate Sponsor'),
        ('community', 'Community Partner'),
    ]

    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='partners/', blank=True, null=True, help_text="Upload partner company/firm logo")
    logo_url = models.URLField(blank=True, help_text="External logo link fallback")
    website = models.URLField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='corporate')
    order = models.PositiveIntegerField(default=0, help_text="Sort order")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Partner & Supporter'
        verbose_name_plural = 'Partners & Supporters'

    def __str__(self):
        return self.name

    @property
    def logo_display(self):
        if self.logo:
            return self.logo.url
        if self.logo_url:
            return self.logo_url
        return None

