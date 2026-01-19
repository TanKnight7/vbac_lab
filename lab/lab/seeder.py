"""
Django Seeder Script for Complete System
Creates: Groups, Users, Posts, and Media files

Run this with: 
  python manage.py shell < seeder.py
Or:
  python manage.py shell
  >>> exec(open('seeder.py').read())
"""

import os
import django
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

# Setup Django environment if running standalone
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lab.settings')
    django.setup()

from django.contrib.auth.models import User, Group
from django.core.files.uploadedfile import SimpleUploadedFile
from post.models import Post
from media.models import Media
from theme.models import Theme
from plugin.models import Plugin

def clear_data():
    """Clear existing data"""
    print("🗑️  Clearing existing data...")
    Plugin.objects.all().delete()
    Theme.objects.all().delete()
    Media.objects.all().delete()
    Post.objects.all().delete()
    User.objects.all().delete()
    print("✅ Data cleared")

def create_groups():
    """Create user groups"""
    print("\n👥 Creating groups...")
    groups = [
        'Super Admin',
        'Administrator', 
        'Editor',
        'Author',
        'Contributor',
        'Subscriber'
    ]
    
    created_groups = []
    for group_name in groups:
        group, created = Group.objects.get_or_create(name=group_name)
        created_groups.append(group)
        status = "✅ Created" if created else "ℹ️  Already exists"
        print(f"  {status}: {group_name}")
    
    return created_groups

def create_users():
    """Create users for each group"""
    print("\n👤 Creating users...")
    
    users_data = [
        {'username': 'superadmin', 'email': 'superadmin@example.com', 'password': 'superadmin', 'group': 'Super Admin'},
        {'username': 'administrator', 'email': 'administrator@example.com', 'password': 'administrator', 'group': 'Administrator'},
        {'username': 'editor', 'email': 'editor@example.com', 'password': 'editor', 'group': 'Editor'},
        {'username': 'author', 'email': 'author@example.com', 'password': 'author', 'group': 'Author'},
        {'username': 'contributor', 'email': 'contributor@example.com', 'password': 'contributor', 'group': 'Contributor'},
        {'username': 'subscriber', 'email': 'subscriber@example.com', 'password': 'subscriber', 'group': 'Subscriber'},
    ]
    
    created_users = {}
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
            }
        )
        
        if created:
            user.set_password(user_data['password'])
            user.save()
        
        # Add to group
        group = Group.objects.get(name=user_data['group'])
        user.groups.add(group)
        
        created_users[user_data['group']] = user
        status = "✅ Created" if created else "ℹ️  Already exists"
        print(f"  {status}: {user.username} ({user_data['group']})")
    
    return created_users

def create_posts(users):
    """Create sample posts"""
    print("\n📝 Creating posts...")
    
    posts_data = [
        # Super Admin posts
        {'title': 'Welcome to Our Blog', 'content': 'This is the first post on our blog! We are excited to share our thoughts with you.', 'author': 'Super Admin', 'status': 'publish'},
        {'title': 'About Our Team', 'content': 'Learn more about the amazing team behind this blog.', 'author': 'Super Admin', 'status': 'publish'},
        
        # Administrator posts
        {'title': 'Site Maintenance Scheduled', 'content': 'We will be performing maintenance on the site next week.', 'author': 'Administrator', 'status': 'publish'},
        {'title': 'New Features Coming Soon', 'content': 'We are working on exciting new features for the blog.', 'author': 'Administrator', 'status': 'draft'},
        {'title': 'Admin Notes', 'content': 'Internal notes for administrators only.', 'author': 'Administrator', 'status': 'private'},
        
        # Editor posts
        {'title': 'Editorial Guidelines', 'content': 'Here are the guidelines for writing articles on our blog.', 'author': 'Editor', 'status': 'publish'},
        {'title': 'Content Calendar for Next Month', 'content': 'Planning the content for the upcoming month.', 'author': 'Editor', 'status': 'draft'},
        {'title': 'Editor\'s Pick: Best Posts', 'content': 'A curated list of the best posts from this month.', 'author': 'Editor', 'status': 'publish'},
        
        # Author posts
        {'title': '10 Tips for Better Writing', 'content': 'Learn how to improve your writing skills with these practical tips.', 'author': 'Author', 'status': 'publish'},
        {'title': 'My Writing Journey', 'content': 'A personal story about my journey as a writer.', 'author': 'Author', 'status': 'publish'},
        {'title': 'Draft: Upcoming Book Review', 'content': 'Working on a review of the latest bestseller.', 'author': 'Author', 'status': 'draft'},
        
        # Contributor posts
        {'title': 'Guest Post: Technology Trends', 'content': 'As a contributor, I want to share insights on technology trends.', 'author': 'Contributor', 'status': 'draft'},
        {'title': 'How to Get Started with Python', 'content': 'A beginner-friendly guide to Python programming.', 'author': 'Contributor', 'status': 'publish'},
        
        # More variety
        {'title': 'The Future of Web Development', 'content': 'Exploring the latest trends in web development including AI, WebAssembly, and more.', 'author': 'Super Admin', 'status': 'publish'},
        {'title': 'Interview with Industry Leaders', 'content': 'We sat down with top professionals to discuss the future.', 'author': 'Editor', 'status': 'publish'},
    ]
    
    created_posts = []
    for post_data in posts_data:
        author = users.get(post_data['author'])
        if not author:
            print(f"  ⚠️  Skipping post '{post_data['title']}' - author not found")
            continue
        
        post = Post.objects.create(
            title=post_data['title'],
            content=post_data['content'],
            author=author,
            status=post_data['status']
        )
        created_posts.append(post)
        print(f"  ✅ Created: {post.title} ({post.status}) by {post.author.username}")
    
    return created_posts


def generate_image(text, color, size=(800, 600)):
    """Generate a simple image with text"""
    img = Image.new('RGB', size, color=color)
    draw = ImageDraw.Draw(img)
    
    # Add text to center
    try:
        # Try to use a default font
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)
    draw.text(position, text, fill='white', font=font)
    
    # Save to bytes
    img_bytes = BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    return img_bytes

def generate_pdf(text):
    """Generate a simple PDF with text"""
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Add text
    p.drawString(100, 750, text)
    p.drawString(100, 730, "This is a sample PDF document.")
    p.drawString(100, 710, "Created by Django Seeder")
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return buffer

def create_media(users):
    """Create sample media files"""
    print("\n🖼️  Creating media files...")
    
    # Check if PIL and reportlab are available
    try:
        from PIL import Image
        pil_available = True
    except ImportError:
        pil_available = False
        print("  ⚠️  Pillow not installed. Install with: pip install Pillow")
    
    try:
        from reportlab.pdfgen import canvas
        reportlab_available = True
    except ImportError:
        reportlab_available = False
        print("  ⚠️  ReportLab not installed. Install with: pip install reportlab")
    
    if not (pil_available and reportlab_available):
        print("  ⚠️  Skipping media creation - required libraries not installed")
        return []
    
    media_data = [
        # Images
        {'name': 'Blog Header Image', 'type': 'image', 'author': 'Super Admin', 'text': 'HEADER', 'color': '#3498db'},
        {'name': 'Team Photo', 'type': 'image', 'author': 'Administrator', 'text': 'TEAM', 'color': '#2ecc71'},
        {'name': 'Article Thumbnail', 'type': 'image', 'author': 'Editor', 'text': 'ARTICLE', 'color': '#e74c3c'},
        {'name': 'Author Profile Picture', 'type': 'image', 'author': 'Author', 'text': 'AUTHOR', 'color': '#f39c12'},
        {'name': 'Featured Image', 'type': 'image', 'author': 'Author', 'text': 'FEATURED', 'color': '#9b59b6'},
        
        # PDFs
        {'name': 'Editorial Guidelines Document', 'type': 'pdf', 'author': 'Editor', 'text': 'Editorial Guidelines'},
        {'name': 'Content Strategy Report', 'type': 'pdf', 'author': 'Administrator', 'text': 'Content Strategy'},
        {'name': 'Writing Tips Handbook', 'type': 'pdf', 'author': 'Author', 'text': 'Writing Tips'},
    ]
    
    created_media = []
    for media_item in media_data:
        author = users.get(media_item['author'])
        if not author:
            print(f"  ⚠️  Skipping media '{media_item['name']}' - author not found")
            continue
        
        try:
            if media_item['type'] == 'image':
                # Generate image
                img_bytes = generate_image(media_item['text'], media_item['color'])
                file = SimpleUploadedFile(
                    name=f"{media_item['name'].replace(' ', '_').lower()}.jpg",
                    content=img_bytes.read(),
                    content_type='image/jpeg'
                )
            else:  # PDF
                # Generate PDF
                pdf_bytes = generate_pdf(media_item['text'])
                file = SimpleUploadedFile(
                    name=f"{media_item['name'].replace(' ', '_').lower()}.pdf",
                    content=pdf_bytes.read(),
                    content_type='application/pdf'
                )
            
            media_obj = Media.objects.create(
                name=media_item['name'],
                file=file,
                author=author
            )
            created_media.append(media_obj)
            print(f"  ✅ Created: {media_obj.name} ({media_item['type']}) by {media_obj.author.username}")
        
        except Exception as e:
            print(f"  ❌ Error creating '{media_item['name']}': {str(e)}")
    
    return created_media

def create_themes():
    """Create sample themes"""
    print("\n🎨 Creating themes...")

    themes_data = [
        {
            'name': 'Default Theme',
            'version': '1.0.0',
            'is_active': True,
            'options': {
                'color_scheme': 'light',
                'show_featured_image': True,
                'layout': 'blog_right_sidebar',
            },
        },
        {
            'name': 'Dark Mode',
            'version': '1.1.0',
            'is_active': False,
            'options': {
                'color_scheme': 'dark',
                'show_featured_image': True,
                'layout': 'full_width',
            },
        },
        {
            'name': 'Minimal',
            'version': '0.9.0',
            'is_active': False,
            'options': {
                'color_scheme': 'light',
                'show_featured_image': False,
                'layout': 'blog_no_sidebar',
            },
        },
    ]

    created_themes = []
    for data in themes_data:
        theme, created = Theme.objects.get_or_create(
            name=data['name'],
            defaults={
                'version': data['version'],
                'is_active': data['is_active'],
                'options': data['options'],
            },
        )
        if not created:
            theme.version = data['version']
            theme.is_active = data['is_active']
            theme.options = data['options']
            theme.save()
        created_themes.append(theme)
        status = "active" if theme.is_active else "installed (inactive)"
        print(f"  ✅ {theme.name} {theme.version} - {status}")

    # Ensure only one active theme (like WordPress)
    active_themes = Theme.objects.filter(is_active=True).order_by('id')
    if active_themes.count() > 1:
        # Keep the first active, deactivate others
        for t in active_themes[1:]:
            t.is_active = False
            t.save()

    return created_themes

def create_plugins():
    """Create sample plugins"""
    print("\n🔌 Creating plugins...")

    plugins_data = [
        {
            'name': 'SEO Optimizer',
            'version': '1.0.0',
            'is_active': True,
            'settings': {
                'meta_description_length': 160,
                'auto_generate_sitemaps': True,
                'focus_keyword_support': True,
            },
        },
        {
            'name': 'Contact Form',
            'version': '2.1.3',
            'is_active': True,
            'settings': {
                'store_entries': True,
                'send_email_notifications': True,
                'spam_protection': 'honeypot',
            },
        },
        {
            'name': 'Analytics Tracker',
            'version': '0.9.5',
            'is_active': False,
            'settings': {
                'provider': 'google_analytics',
                'anonymize_ip': True,
            },
        },
        {
            'name': 'Cache Booster',
            'version': '1.2.0',
            'is_active': False,
            'settings': {
                'enable_page_cache': True,
                'minify_css': True,
                'minify_js': True,
            },
        },
    ]

    created_plugins = []
    for data in plugins_data:
        plugin, created = Plugin.objects.get_or_create(
            name=data['name'],
            defaults={
                'version': data['version'],
                'is_active': data['is_active'],
                'settings': data['settings'],
            },
        )
        if not created:
            plugin.version = data['version']
            plugin.is_active = data['is_active']
            plugin.settings = data['settings']
            plugin.save()
        created_plugins.append(plugin)
        status = "activated" if plugin.is_active else "installed (inactive)"
        print(f"  ✅ {plugin.name} {plugin.version} - {status}")

    return created_plugins


def print_summary(users, posts, media, themes, plugins):
    """Print summary of seeded data"""
    print("\n" + "="*60)
    print("📊 SEEDING SUMMARY")
    print("="*60)
    
    print(f"\n👥 Users created: {len(users)}")
    for group, user in users.items():
        print(f"   • {user.username} - {group}")
    
    print(f"\n📝 Posts created: {len(posts)}")
    print(f"   • Published: {sum(1 for p in posts if p.status == 'publish')}")
    print(f"   • Draft: {sum(1 for p in posts if p.status == 'draft')}")
    print(f"   • Private: {sum(1 for p in posts if p.status == 'private')}")
    
    print(f"\n🖼️  Media files created: {len(media)}")
    if media:
        # Count by file type
        image_count = sum(1 for m in media if m.file.name.endswith(('.jpg', '.png')))
        pdf_count = sum(1 for m in media if m.file.name.endswith('.pdf'))
        print(f"   • Images: {image_count}")
        print(f"   • PDFs: {pdf_count}")

    print(f"\n🎨 Themes created: {len(themes)}")
    if themes:
        active = sum(1 for t in themes if t.is_active)
        print(f"   • Active: {active}")
        print(f"   • Inactive: {len(themes) - active}")

    print(f"\n🔌 Plugins created: {len(plugins)}")
    if plugins:
        active_plugins = sum(1 for p in plugins if p.is_active)
        print(f"   • Active: {active_plugins}")
        print(f"   • Inactive: {len(plugins) - active_plugins}")
    
    print("\n🔐 Login Credentials:")
    print("   All users have password as username")
    print("   Examples:")
    for group, user in list(users.items())[:3]:
        print(f"   • Username: {user.username}, Password: {user.username}")
    
    print("\n📦 Required packages:")
    print("   • pip install Pillow (for images)")
    print("   • pip install reportlab (for PDFs)")
    
    print("\n" + "="*60)
    print("✅ Seeding completed successfully!")
    print("="*60)

def run_seeder(clear_existing=True):
    """Main seeder function"""
    print("="*60)
    print("🌱 DJANGO SEEDER - COMPLETE SYSTEM")
    print("="*60)
    
    if clear_existing:
        clear_data()
    
    groups = create_groups()
    users = create_users()
    posts = create_posts(users)
    media = create_media(users)
    themes = create_themes()
    plugins = create_plugins()

    print_summary(users, posts, media, themes, plugins)

if __name__ == '__main__':
    # Run the seeder
    run_seeder(clear_existing=True)
else:
    # If imported in Django shell
    print("Seeder loaded. Run: run_seeder() to seed the database")
    print("Or run: run_seeder(clear_existing=False) to keep existing data")

