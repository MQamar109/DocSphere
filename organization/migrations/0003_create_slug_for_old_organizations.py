from django.db import migrations
from django.utils.text import slugify

def create_slug_for_old_organizations(apps, schema_editor):
    organization_model = apps.get_model('organization', 'Organization')
    for organization in organization_model.objects.all():
        organization.slug = slugify(organization.name)
        organization.save()

def reverse_create_slug_for_old_organizations(apps, schema_editor):
    organization_model = apps.get_model('organization', 'Organization')
    for organization in organization_model.objects.all():
        organization.slug = None
        organization.save()

class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_organization_slug'),
    ]

    operations = [
        migrations.RunPython(create_slug_for_old_organizations, reverse_create_slug_for_old_organizations)
    ]
