import glob
import re

files = glob.glob('*.html')
for f in sorted(files):
    with open(f, 'r', encoding='utf-8') as fp:
        c = fp.read()
    after_footer = c.split('</footer>')[-1] if '</footer>' in c else ''
    scripts = re.findall(r'<script[^>]*>.*?</script>', after_footer, re.DOTALL)
    external_scripts = re.findall(r'<script[^>]+src=["\'][^"\']+["\'][^>]*>', c)
    title_match = re.search(r'<title>(.*?)</title>', c)
    title = title_match.group(1) if title_match else f
    print(f"{f:25} | ExtScripts: {len(external_scripts)} | AfterFooterScripts: {len(scripts)} | Title: {title[:40]}")
