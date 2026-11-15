import os
import re

PAGE_MAPPING = {
    'index.html': ('core/index.html', 'home'),
    'about.html': ('core/about.html', 'about'),
    'leadership.html': ('core/leadership.html', 'leadership'),
    'contact.html': ('core/contact.html', 'contact'),
    'gallery.html': ('core/gallery.html', 'gallery'),
    'donate.html': ('core/donate.html', 'donate'),
    'campus.html': ('members/campus.html', 'chapters'),
    'registration.html': ('members/registration.html', 'register'),
    'news.html': ('news/news_list.html', 'news_list'),
    'news_details_view.html': ('news/news_detail.html', 'news_detail'),
    'program.html': ('programs/program_list.html', 'programs'),
    'scholarship.html': ('programs/scholarship_list.html', 'scholarships'),
    'resources.html': ('programs/resource_list.html', 'resources'),
}

LINK_REPLACEMENTS = [
    (r'href=["\']index\.html["\']', "href=\"{% url 'home' %}\""),
    (r'href=["\']about\.html["\']', "href=\"{% url 'about' %}\""),
    (r'href=["\']leadership\.html["\']', "href=\"{% url 'leadership' %}\""),
    (r'href=["\']campus\.html["\']', "href=\"{% url 'chapters' %}\""),
    (r'href=["\']chapters\.html["\']', "href=\"{% url 'chapters' %}\""),
    (r'href=["\']program\.html["\']', "href=\"{% url 'programs' %}\""),
    (r'href=["\']programmes\.html["\']', "href=\"{% url 'programs' %}\""),
    (r'href=["\']news\.html["\']', "href=\"{% url 'news_list' %}\""),
    (r'href=["\']news_details_view\.html["\']', "href=\"{% url 'news_list' %}\""),
    (r'href=["\']scholarship\.html["\']', "href=\"{% url 'scholarships' %}\""),
    (r'href=["\']scholarships\.html["\']', "href=\"{% url 'scholarships' %}\""),
    (r'href=["\']gallery\.html["\']', "href=\"{% url 'gallery' %}\""),
    (r'href=["\']resources\.html["\']', "href=\"{% url 'resources' %}\""),
    (r'href=["\']contact\.html["\']', "href=\"{% url 'contact' %}\""),
    (r'href=["\']donate\.html["\']', "href=\"{% url 'donate' %}\""),
    (r'href=["\']registration\.html["\']', "href=\"{% url 'register' %}\""),
    (r'href=["\']join\.html["\']', "href=\"{% url 'register' %}\""),
]

def convert_page(src_filename, dest_relpath):
    with open(src_filename, 'r', encoding='utf-8') as f:
        html = f.read()

    # Extract title
    title_match = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
    title = title_match.group(1).strip() if title_match else 'NABAS'

    # Extract external script tags (e.g. tailwind, lucide)
    ext_scripts = re.findall(r'<script[^>]+src=["\'][^"\']+["\'][^>]*>\s*</script>', html)
    ext_scripts_html = "\n".join(ext_scripts)

    # Extract style block(s)
    styles = re.findall(r'<style[^>]*>(.*?)</style>', html, re.DOTALL)
    combined_css = "\n".join(styles).strip()

    # Extract main content: between </header> and <footer
    header_end = html.find('</header>')
    footer_start = html.rfind('<footer')

    if header_end != -1 and footer_start != -1:
        body_content = html[header_end + len('</header>'):footer_start].strip()
    else:
        # Fallback if structure varies
        body_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL)
        body_content = body_match.group(1).strip() if body_match else html

    # Extract any modals or content between </footer> and </body>
    footer_end = html.rfind('</footer>')
    after_footer = html[footer_end + len('</footer>'):] if footer_end != -1 else ''
    
    # Extract scripts after footer
    inline_scripts = re.findall(r'<script[^>]*>(.*?)</script>', after_footer, re.DOTALL)
    combined_js = "\n".join(inline_scripts).strip()
    
    # Remove mobile menu toggle & scroll header code from page-specific JS since base.html handles it
    clean_js = combined_js
    clean_js = re.sub(r'const mobileBtn = document\.getElementById\([\'"]mobileMenuBtn[\'"]\);.*?(?=const|\bfunction\b|\blet\b|\bvar\b|$)', '', clean_js, flags=re.DOTALL)
    clean_js = re.sub(r'window\.addEventListener\([\'"]scroll[\'"].*?\}\);', '', clean_js, flags=re.DOTALL)

    # Any non-script markup between </footer> and </body> (e.g. search modal)
    non_script_after_footer = re.sub(r'<script[^>]*>.*?</script>', '', after_footer, flags=re.DOTALL)
    non_script_after_footer = re.sub(r'</body>|</html>', '', non_script_after_footer).strip()

    full_content = body_content
    if non_script_after_footer:
        full_content += "\n\n" + non_script_after_footer

    # Apply link replacements
    for pattern, repl in LINK_REPLACEMENTS:
        full_content = re.sub(pattern, repl, full_content)

    # Add CSRF token to form tags
    full_content = re.sub(r'(<form[^>]*>)', r'\1\n  {% csrf_token %}', full_content)

    # Build the template
    template_parts = ["{% extends 'base.html' %}", ""]
    template_parts.append(f"{{% block title %}}{title}{{% endblock %}}")
    template_parts.append("")

    if ext_scripts_html or combined_css:
        template_parts.append("{% block extra_css %}")
        if ext_scripts_html:
            template_parts.append(ext_scripts_html)
        if combined_css:
            template_parts.append("<style>")
            template_parts.append(combined_css)
            template_parts.append("</style>")
        template_parts.append("{% endblock %}")
        template_parts.append("")

    template_parts.append("{% block content %}")
    template_parts.append(full_content)
    template_parts.append("{% endblock %}")
    template_parts.append("")

    if clean_js.strip():
        template_parts.append("{% block extra_js %}")
        template_parts.append("<script>")
        template_parts.append(clean_js.strip())
        template_parts.append("</script>")
        template_parts.append("{% endblock %}")
        template_parts.append("")

    dest_path = os.path.join('templates', dest_relpath)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(template_parts))

    print(f"Converted {src_filename} -> {dest_path}")

def main():
    for src, (dest, _) in PAGE_MAPPING.items():
        if os.path.exists(src):
            convert_page(src, dest)
        else:
            print(f"File not found: {src}")

if __name__ == '__main__':
    main()
