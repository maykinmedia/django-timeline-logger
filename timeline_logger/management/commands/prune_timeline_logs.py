from datetime import datetime
from textwrap import dedent

from django.core.management.base import BaseCommand

from timeline_logger.models import TimelineLog


class Command(BaseCommand):
    help = "Removes timeline logs objects older than the specified date."

    def add_arguments(self, parser):
        parser.add_argument(
            "--noinput",
            "--no-input",
            action="store_false",
            dest="interactive",
            help="Tells Django to NOT prompt the user for input of any kind.",
        )
        parser.add_argument(
            "--before",
            type=datetime.fromisoformat,
            help="Only flush timeline logs older than the specified date.",
        )

    def handle(self, *args, **options):
        interactive = options["interactive"]
        before = options["before"]

        if not before and interactive:
            confirm = input(
                dedent(
                    """You haven't specified a date to limit the objects to be deleted.
                This will delete all timeline logs objects. Are you sure you want to do this?

                Type 'yes' to continue, or 'no' to cancel: """
                )
            )
        else:
            confirm = "yes"

        if confirm == "yes":
            if before:
                qs = TimelineLog.objects.filter(timestamp__lte=before)
            else:
                qs = TimelineLog.objects.all()
            number, _ = qs.delete()
            self.stdout.write(f"Successfully deleted {number} timeline logs.")
        else:
            self.stdout.write("Flush cancelled.")
