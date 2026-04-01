from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("organization", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="organization",
            name="admin_email",
            field=models.EmailField(
                max_length=254, null=True, blank=True, unique=True
            ),
        ),
    ]
