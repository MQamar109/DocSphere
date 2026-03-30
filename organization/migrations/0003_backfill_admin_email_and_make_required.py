from django.db import migrations, models


def backfill_admin_email(apps, schema_editor):
    Organization = apps.get_model("organization", "Organization")

    for org in Organization.objects.filter(admin_email__isnull=True):
        # Use a deterministic, unique placeholder per organization.
        org.admin_email = f"org-{org.pk}@example.local"
        org.save(update_fields=["admin_email"])


class Migration(migrations.Migration):
    dependencies = [
        ("organization", "0002_organization_admin_email_nullable"),
    ]

    operations = [
        migrations.RunPython(
            code=backfill_admin_email,
            reverse_code=migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name="organization",
            name="admin_email",
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
