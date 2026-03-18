from django.core.management.base import BaseCommand

from organization.models import Organization


class Command(BaseCommand):
    help = "Fill data in the organization"

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simulate the commands action',
        )
        parser.add_argument(
            'count',
            type=int,
            help="Count of the rows to fill in the organization",
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        count = options['count']

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    "here is the data will be filled to the DB"
                )
            )
            self.stdout.write(
                f"{self.get_organization_data(count)}"
            )
        else:
            Organization.objects.bulk_create(
                self.get_organization_data(count)
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"{count} records has been updated"
                    " in organization"
                )
            )

    def get_organization_data(self, count):
        return [
            Organization(
                name=f"organization #{i}",
                description=f"description #{i}",
                is_active=bool(i % 2),
            )
            for i in range(count)
        ]
