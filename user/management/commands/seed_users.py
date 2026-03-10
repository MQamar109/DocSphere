import random

from django.core.management.base import BaseCommand

from organization.models import Organization
from user.models import User
from user.choices import USER_ROLE_OPTIONS


class Command(BaseCommand): 
    help = "Fill data in the users"

    def add_arguments(self, parser):
        parser.add_argument(
            "count",
            type=int,
            help="Count of the rows to fill in the users",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Simulate the commands action",
        )

    def handle(self, *args, **options):
        count = options["count"]
        dry_run = options["dry_run"]
        if dry_run:
            self.stdout.write(self.style.WARNING("here is the data will be filled to the DB"))
            self.stdout.write(f"{self.seed_users(count)}")
        else:
            User.objects.bulk_create(self.seed_users(count))
            self.stdout.write(self.style.SUCCESS(f"{count} records has been updated in users"))


    def seed_users(self, count):
        users = []
        organization = Organization.objects.first()

        for i in range(count):
            user = User(
                email=f"user{i}@example.com",
                organization=organization,
                role=random.choice([choice[0] for choice in USER_ROLE_OPTIONS]),
            )
            user.set_password(f"password{i}")
            users.append(user)

        return users
