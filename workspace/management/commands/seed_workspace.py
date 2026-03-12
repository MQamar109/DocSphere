import random

from django.core.management.base import BaseCommand

from organization.models import Organization
from user.models import User
from workspace.models import (
    Project,
    Document,
    ProjectPermissions,
    DocumentPermissions,
)
from workspace.choices import (
    PROJECT_PERMISSIONS_OPTIONS,
    DOCUMENT_PERMISSIONS_OPTIONS,
)


class Command(BaseCommand):
    help = "Fill data in the workspace"

    def add_arguments(self, parser):
        parser.add_argument(
            "count",
            type=int,
            help="Count of the rows to fill in the project and document",
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
            self.stdout.write(f"{self.seed_project(count)}")
            self.stdout.write(f"{self.seed_document(count)}")
            self.stdout.write(
                f"Would create {count} ProjectPermissions and {count} DocumentPermissions"
            )
        else:
            Project.objects.bulk_create(self.seed_project(count))
            Document.objects.bulk_create(self.seed_document(count))
            ProjectPermissions.objects.bulk_create(self.seed_project_permissions(count))
            DocumentPermissions.objects.bulk_create(self.seed_document_permissions(count))
            self.stdout.write(self.style.SUCCESS(f"{count} records has been updated in project and document and added permissions"))

    def seed_project(self, count):
        organization = Organization.objects.first()
        return [
            Project(
                name=f"project #{i}",
                description=f"description #{i}",
                organization=organization,
            )
            for i in range(count)
        ]

    def seed_document(self, count):
        project = Project.objects.first()
        return [
            Document(
                name=f"document #{i}",
                description=f"description #{i}",
                project=project,
            )
            for i in range(count)
        ]

    def seed_project_permissions(self, count):
        project = Project.objects.first()
        user = User.objects.first()
        return [
            ProjectPermissions(
                project=project,
                user=user,
                permissions=random.choice([choice[0] for choice in PROJECT_PERMISSIONS_OPTIONS]),
            )
            for i in range(count)
        ]

    def seed_document_permissions(self, count):
        document = Document.objects.first()
        user = User.objects.first()
        return [
            DocumentPermissions(
                document=document,
                user=user,
                permissions=random.choice([choice[0] for choice in DOCUMENT_PERMISSIONS_OPTIONS]),
            )
            for i in range(count)
        ]
