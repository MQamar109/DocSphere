from django.db import migrations, models
from django.db.models import Q
from django.utils.text import slugify


def backfill_null_slugs(apps, schema_editor):
    Organization = apps.get_model("organization", "Organization")
    qs = Organization.objects.filter(Q(slug__isnull=True) | Q(slug=""))
    for org in qs.iterator():
        base = slugify(org.name) or f"org-{org.pk}"
        candidate = base
        suffix = 1
        while (
            Organization.objects.filter(slug=candidate)
            .exclude(pk=org.pk)
            .exists()
        ):
            candidate = f"{base}-{suffix}"
            suffix += 1
        org.slug = candidate
        org.save(update_fields=["slug"])


class Migration(migrations.Migration):

    dependencies = [
        ("organization", "0004_merge_20260330_1244"),
    ]

    operations = [
        migrations.RunPython(
            code=backfill_null_slugs,
            reverse_code=migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name="organization",
            name="slug",
            field=models.SlugField(blank=True, max_length=50, unique=True),
        ),
    ]
