#!/usr/bin/env python
"""
Build script for generating static site with all language variants.

This script generates static HTML files for all pages in all supported
languages (en, fa, ar) for deployment to GitHub Pages.

Usage:
    python build_static.py

Output:
    dist/
    ├── index.html          # Redirect to /en/
    ├── .nojekyll           # Disable Jekyll processing
    ├── CNAME               # Custom domain
    ├── static/website/     # CSS, JS, fonts, images
    ├── media/              # Uploaded images
    ├── en/                 # English pages
    ├── fa/                 # Persian pages (RTL)
    └── ar/                 # Arabic pages (RTL)
"""

import os
import sys
import shutil

# Set environment for static build BEFORE importing Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rabani.settings')
os.environ['BUILD_STATIC'] = 'True'

import django
django.setup()

from django.conf import settings
from django.utils import translation
from django.template import loader
from django.template import Context
from website.models import SlideShowImage, PatientImage, GalleryImage, Course

# Configuration
OUTPUT_DIR = 'dist'
CUSTOM_DOMAIN = 'drrabani.com'
LANGUAGES = ['en', 'fa']
DEFAULT_LANGUAGE = 'fa'
# Base URL for GitHub Pages project site (empty string for custom domain)
# When using custom domain (drrabani.com), BASE_URL should be empty
# When using github.io subdirectory, BASE_URL should be '/rabaniDjango'
BASE_URL = os.environ.get('BASE_URL', '')


def clean_output():
    """Remove and recreate output directory."""
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)
    print(f'Created output directory: {OUTPUT_DIR}/')


def get_base_context():
    """Get common context variables used across all templates."""
    return {
        'dr_email': 'parham.davarii@gmail.com',
        'dr_phone': '+989033103516',
        'dr_instagram': 'https://www.instagram.com/dr.hossein.rabbani/',
        'clinic_instagram': 'https://www.instagram.com/dr.hossein.rabbani/',
        'clinic_addr': 'Unit 1, 8th Floor, Jaam-e-Jam Complex, East Pahlavan St., Ahvaz, Khuzestan, Iran',
        'welcome_msg': 'Follow us on social media for updates, personalized care, and to make reservation!',
        'GA_KEY': os.environ.get('GOOGLE_ANALYTICS_KEY', ''),
        'BASE_URL': BASE_URL,
    }


def render_template(template_name, context, lang):
    """Render a template with the given context and language."""
    translation.activate(lang)

    # Add language code to context
    context['LANGUAGE_CODE'] = lang

    template = loader.get_template(template_name)
    html = template.render(context)

    translation.deactivate()
    return html


def setup_database():
    """Ensure database tables exist."""
    from django.core.management import call_command
    try:
        # Run migrations to create tables
        call_command('migrate', '--run-syncdb', verbosity=0)
        print('Database ready.')
    except Exception as e:
        print(f'Database setup warning: {e}')


def generate_pages():
    """Generate HTML pages for all languages."""
    base_context = get_base_context()

    # Fetch database content once (may be empty in CI)
    try:
        slideshow_images = list(SlideShowImage.objects.all())
        patient_images = list(PatientImage.objects.all())
        gallery_images = list(GalleryImage.objects.all())
        courses = list(Course.objects.all())
    except Exception as e:
        print(f'Warning: Could not fetch database content: {e}')
        slideshow_images = []
        patient_images = []
        gallery_images = []
        courses = []

    for lang in LANGUAGES:
        lang_dir = os.path.join(OUTPUT_DIR, lang)
        os.makedirs(lang_dir, exist_ok=True)

        print(f'\nGenerating pages for language: {lang}')

        # Home page
        context = {
            **base_context,
            'PAGE_NAME': 'home',
            'slideshow_images': slideshow_images,
            'patient_images': patient_images,
            'gallery_images': gallery_images,
        }
        try:
            html = render_template('templates_static/home.html', context, lang)
            with open(os.path.join(lang_dir, 'index.html'), 'w', encoding='utf-8') as f:
                f.write(html)
            print(f'  Generated: {lang}/index.html')

            with open(os.path.join(lang_dir, 'home.html'), 'w', encoding='utf-8') as f:
                f.write(html)
            print(f'  Generated: {lang}/home.html')
        except Exception as e:
            print(f'  Error generating home: {e}')

        # About page
        context = {**base_context, 'PAGE_NAME': 'about'}
        try:
            html = render_template('templates_static/about.html', context, lang)
            with open(os.path.join(lang_dir, 'about.html'), 'w', encoding='utf-8') as f:
                f.write(html)
            print(f'  Generated: {lang}/about.html')
        except Exception as e:
            print(f'  Error generating about: {e}')

        # Contact page
        context = {**base_context, 'PAGE_NAME': 'contact'}
        try:
            html = render_template('templates_static/contact.html', context, lang)
            with open(os.path.join(lang_dir, 'contact.html'), 'w', encoding='utf-8') as f:
                f.write(html)
            print(f'  Generated: {lang}/contact.html')
        except Exception as e:
            print(f'  Error generating contact: {e}')

        # Courses page
        context = {
            **base_context,
            'PAGE_NAME': 'courses',
            'courses': courses,
        }
        try:
            html = render_template('templates_static/courses.html', context, lang)
            with open(os.path.join(lang_dir, 'courses.html'), 'w', encoding='utf-8') as f:
                f.write(html)
            print(f'  Generated: {lang}/courses.html')
        except Exception as e:
            print(f'  Error generating courses: {e}')

        # Appointment page
        context = {**base_context, 'PAGE_NAME': 'appointment'}
        try:
            html = render_template('templates_static/appointment.html', context, lang)
            with open(os.path.join(lang_dir, 'appointment.html'), 'w', encoding='utf-8') as f:
                f.write(html)
            print(f'  Generated: {lang}/appointment.html')
        except Exception as e:
            print(f'  Error generating appointment: {e}')


def copy_static():
    """Copy static files to output directory."""
    src = os.path.join(settings.BASE_DIR, 'static')
    dst = os.path.join(OUTPUT_DIR, 'static')

    if os.path.exists(src):
        shutil.copytree(src, dst)
        print(f'\nCopied static files to {dst}/')
    else:
        print(f'\nWarning: Static directory not found at {src}')


def copy_media():
    """Copy media files to output directory."""
    src = settings.MEDIA_ROOT
    dst = os.path.join(OUTPUT_DIR, 'media')

    if os.path.exists(src):
        shutil.copytree(src, dst)
        print(f'Copied media files to {dst}/')
    else:
        print(f'Warning: Media directory not found at {src}')


def create_github_pages_files():
    """Create necessary GitHub Pages configuration files."""
    print('\nCreating GitHub Pages configuration files...')

    # .nojekyll - prevents Jekyll processing
    nojekyll_path = os.path.join(OUTPUT_DIR, '.nojekyll')
    open(nojekyll_path, 'w').close()
    print('  Created .nojekyll')

    # CNAME - custom domain
    cname_path = os.path.join(OUTPUT_DIR, 'CNAME')
    with open(cname_path, 'w') as f:
        f.write(CUSTOM_DOMAIN)
    print(f'  Created CNAME ({CUSTOM_DOMAIN})')

    # Root index.html - redirect to default language
    redirect_url = f'{BASE_URL}/{DEFAULT_LANGUAGE}/'
    redirect_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="0; url={redirect_url}">
    <link rel="canonical" href="https://{CUSTOM_DOMAIN}/{DEFAULT_LANGUAGE}/">
    <script>window.location.href = '{redirect_url}';</script>
    <title>Redirecting to Dr. Rabbani's Website</title>
</head>
<body>
    <p>Redirecting to <a href="{redirect_url}">Dr. Rabbani's Website</a>...</p>
</body>
</html>'''

    index_path = os.path.join(OUTPUT_DIR, 'index.html')
    with open(index_path, 'w') as f:
        f.write(redirect_html)
    print(f'  Created root index.html (redirects to {redirect_url})')


def create_404_page():
    """Create a custom 404 page."""
    html_404 = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Page Not Found - Dr. Rabbani</title>
    <style>
        body {{
            font-family: 'Open Sans', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: #f5f5f5;
        }}
        .container {{
            text-align: center;
            padding: 40px;
        }}
        h1 {{
            font-size: 72px;
            margin: 0;
            color: #333;
        }}
        p {{
            font-size: 18px;
            color: #666;
        }}
        a {{
            color: #007bff;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>404</h1>
        <p>Page not found</p>
        <p><a href="{BASE_URL}/{DEFAULT_LANGUAGE}/">Go to Homepage</a></p>
    </div>
</body>
</html>'''

    path_404 = os.path.join(OUTPUT_DIR, '404.html')
    with open(path_404, 'w') as f:
        f.write(html_404)
    print('  Created 404.html')


def print_summary():
    """Print build summary."""
    print('\n' + '=' * 50)
    print('BUILD COMPLETE')
    print('=' * 50)
    print(f'Output directory: {OUTPUT_DIR}/')
    print(f'Custom domain: {CUSTOM_DOMAIN}')
    print(f'Languages: {", ".join(LANGUAGES)}')
    print(f'Default language: {DEFAULT_LANGUAGE}')
    print('\nTo test locally:')
    print(f'  cd {OUTPUT_DIR} && python -m http.server 8000')
    print('  Then visit: http://localhost:8000/')
    print('\nTo deploy:')
    print('  Push to GitHub and configure GitHub Pages')
    print('=' * 50)


def main():
    """Main build function."""
    print('=' * 50)
    print('STATIC SITE BUILDER')
    print('Dr. Rabbani Dental Clinic')
    print('=' * 50)

    # Step 1: Clean output directory
    clean_output()

    # Step 2: Setup database (run migrations)
    setup_database()

    # Step 3: Generate pages for all languages
    generate_pages()

    # Step 3: Copy static files
    copy_static()

    # Step 4: Copy media files
    copy_media()

    # Step 5: Create GitHub Pages files
    create_github_pages_files()

    # Step 6: Create 404 page
    create_404_page()

    # Step 7: Print summary
    print_summary()


if __name__ == '__main__':
    main()
